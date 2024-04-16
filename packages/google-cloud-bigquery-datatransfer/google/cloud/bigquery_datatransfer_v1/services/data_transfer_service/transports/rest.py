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
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.bigquery_datatransfer_v1.types import datatransfer, transfer

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DataTransferServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class DataTransferServiceRestInterceptor:
    """Interceptor for DataTransferService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DataTransferServiceRestTransport.

    .. code-block:: python
        class MyCustomDataTransferServiceInterceptor(DataTransferServiceRestInterceptor):
            def pre_check_valid_creds(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_valid_creds(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_transfer_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_transfer_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_transfer_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_transfer_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_enroll_data_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_transfer_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_transfer_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_transfer_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_transfer_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_data_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_transfer_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_transfer_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_transfer_logs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_transfer_logs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_transfer_runs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_transfer_runs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_schedule_transfer_runs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_schedule_transfer_runs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_manual_transfer_runs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_manual_transfer_runs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_unenroll_data_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_update_transfer_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_transfer_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DataTransferServiceRestTransport(interceptor=MyCustomDataTransferServiceInterceptor())
        client = DataTransferServiceClient(transport=transport)


    """

    def pre_check_valid_creds(
        self,
        request: datatransfer.CheckValidCredsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.CheckValidCredsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for check_valid_creds

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_check_valid_creds(
        self, response: datatransfer.CheckValidCredsResponse
    ) -> datatransfer.CheckValidCredsResponse:
        """Post-rpc interceptor for check_valid_creds

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_create_transfer_config(
        self,
        request: datatransfer.CreateTransferConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.CreateTransferConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_transfer_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_create_transfer_config(
        self, response: transfer.TransferConfig
    ) -> transfer.TransferConfig:
        """Post-rpc interceptor for create_transfer_config

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_transfer_config(
        self,
        request: datatransfer.DeleteTransferConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.DeleteTransferConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_transfer_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def pre_delete_transfer_run(
        self,
        request: datatransfer.DeleteTransferRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.DeleteTransferRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_transfer_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def pre_enroll_data_sources(
        self,
        request: datatransfer.EnrollDataSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.EnrollDataSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for enroll_data_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def pre_get_data_source(
        self,
        request: datatransfer.GetDataSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.GetDataSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_get_data_source(
        self, response: datatransfer.DataSource
    ) -> datatransfer.DataSource:
        """Post-rpc interceptor for get_data_source

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_get_transfer_config(
        self,
        request: datatransfer.GetTransferConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.GetTransferConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_transfer_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_get_transfer_config(
        self, response: transfer.TransferConfig
    ) -> transfer.TransferConfig:
        """Post-rpc interceptor for get_transfer_config

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_get_transfer_run(
        self,
        request: datatransfer.GetTransferRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.GetTransferRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_transfer_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_get_transfer_run(
        self, response: transfer.TransferRun
    ) -> transfer.TransferRun:
        """Post-rpc interceptor for get_transfer_run

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_list_data_sources(
        self,
        request: datatransfer.ListDataSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.ListDataSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_data_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_list_data_sources(
        self, response: datatransfer.ListDataSourcesResponse
    ) -> datatransfer.ListDataSourcesResponse:
        """Post-rpc interceptor for list_data_sources

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_list_transfer_configs(
        self,
        request: datatransfer.ListTransferConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.ListTransferConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_transfer_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_list_transfer_configs(
        self, response: datatransfer.ListTransferConfigsResponse
    ) -> datatransfer.ListTransferConfigsResponse:
        """Post-rpc interceptor for list_transfer_configs

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_list_transfer_logs(
        self,
        request: datatransfer.ListTransferLogsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.ListTransferLogsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_transfer_logs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_list_transfer_logs(
        self, response: datatransfer.ListTransferLogsResponse
    ) -> datatransfer.ListTransferLogsResponse:
        """Post-rpc interceptor for list_transfer_logs

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_list_transfer_runs(
        self,
        request: datatransfer.ListTransferRunsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.ListTransferRunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_transfer_runs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_list_transfer_runs(
        self, response: datatransfer.ListTransferRunsResponse
    ) -> datatransfer.ListTransferRunsResponse:
        """Post-rpc interceptor for list_transfer_runs

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_schedule_transfer_runs(
        self,
        request: datatransfer.ScheduleTransferRunsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.ScheduleTransferRunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for schedule_transfer_runs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_schedule_transfer_runs(
        self, response: datatransfer.ScheduleTransferRunsResponse
    ) -> datatransfer.ScheduleTransferRunsResponse:
        """Post-rpc interceptor for schedule_transfer_runs

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_start_manual_transfer_runs(
        self,
        request: datatransfer.StartManualTransferRunsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.StartManualTransferRunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_manual_transfer_runs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_start_manual_transfer_runs(
        self, response: datatransfer.StartManualTransferRunsResponse
    ) -> datatransfer.StartManualTransferRunsResponse:
        """Post-rpc interceptor for start_manual_transfer_runs

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_unenroll_data_sources(
        self,
        request: datatransfer.UnenrollDataSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.UnenrollDataSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for unenroll_data_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def pre_update_transfer_config(
        self,
        request: datatransfer.UpdateTransferConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datatransfer.UpdateTransferConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_transfer_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_update_transfer_config(
        self, response: transfer.TransferConfig
    ) -> transfer.TransferConfig:
        """Post-rpc interceptor for update_transfer_config

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
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
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
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
        before they are sent to the DataTransferService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the DataTransferService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DataTransferServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataTransferServiceRestInterceptor


class DataTransferServiceRestTransport(DataTransferServiceTransport):
    """REST backend transport for DataTransferService.

    This API allows users to manage their data transfers into
    BigQuery.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "bigquerydatatransfer.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DataTransferServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigquerydatatransfer.googleapis.com').
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
        self._interceptor = interceptor or DataTransferServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CheckValidCreds(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("CheckValidCreds")

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
            request: datatransfer.CheckValidCredsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.CheckValidCredsResponse:
            r"""Call the check valid creds method over HTTP.

            Args:
                request (~.datatransfer.CheckValidCredsRequest):
                    The request object. A request to determine whether the
                user has valid credentials. This method
                is used to limit the number of OAuth
                popups in the user interface. The user
                id is inferred from the API call
                context. If the data source has the
                Google+ authorization type, this method
                returns false, as it cannot be
                determined whether the credentials are
                already valid merely based on the user
                id.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datatransfer.CheckValidCredsResponse:
                    A response indicating whether the
                credentials exist and are valid.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/dataSources/*}:checkValidCreds",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/dataSources/*}:checkValidCreds",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_check_valid_creds(
                request, metadata
            )
            pb_request = datatransfer.CheckValidCredsRequest.pb(request)
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
            resp = datatransfer.CheckValidCredsResponse()
            pb_resp = datatransfer.CheckValidCredsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_check_valid_creds(resp)
            return resp

    class _CreateTransferConfig(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("CreateTransferConfig")

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
            request: datatransfer.CreateTransferConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer.TransferConfig:
            r"""Call the create transfer config method over HTTP.

            Args:
                request (~.datatransfer.CreateTransferConfigRequest):
                    The request object. A request to create a data transfer
                configuration. If new credentials are
                needed for this transfer configuration,
                authorization info must be provided. If
                authorization info is provided, the
                transfer configuration will be
                associated with the user id
                corresponding to the authorization info.
                Otherwise, the transfer configuration
                will be associated with the calling
                user.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer.TransferConfig:
                    Represents a data transfer configuration. A transfer
                configuration contains all metadata needed to perform a
                data transfer. For example, ``destination_dataset_id``
                specifies where data should be stored. When a new
                transfer configuration is created, the specified
                ``destination_dataset_id`` is created when needed and
                shared with the appropriate data source service account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/transferConfigs",
                    "body": "transfer_config",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/transferConfigs",
                    "body": "transfer_config",
                },
            ]
            request, metadata = self._interceptor.pre_create_transfer_config(
                request, metadata
            )
            pb_request = datatransfer.CreateTransferConfigRequest.pb(request)
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
            resp = transfer.TransferConfig()
            pb_resp = transfer.TransferConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_transfer_config(resp)
            return resp

    class _DeleteTransferConfig(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("DeleteTransferConfig")

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
            request: datatransfer.DeleteTransferConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete transfer config method over HTTP.

            Args:
                request (~.datatransfer.DeleteTransferConfigRequest):
                    The request object. A request to delete data transfer
                information. All associated transfer
                runs and log messages will be deleted as
                well.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/transferConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/transferConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_transfer_config(
                request, metadata
            )
            pb_request = datatransfer.DeleteTransferConfigRequest.pb(request)
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

    class _DeleteTransferRun(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("DeleteTransferRun")

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
            request: datatransfer.DeleteTransferRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete transfer run method over HTTP.

            Args:
                request (~.datatransfer.DeleteTransferRunRequest):
                    The request object. A request to delete data transfer run
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/transferConfigs/*/runs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/transferConfigs/*/runs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_transfer_run(
                request, metadata
            )
            pb_request = datatransfer.DeleteTransferRunRequest.pb(request)
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

    class _EnrollDataSources(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("EnrollDataSources")

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
            request: datatransfer.EnrollDataSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the enroll data sources method over HTTP.

            Args:
                request (~.datatransfer.EnrollDataSourcesRequest):
                    The request object. A request to enroll a set of data sources so they are
                visible in the BigQuery UI's ``Transfer`` tab.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*}:enrollDataSources",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*}:enrollDataSources",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_enroll_data_sources(
                request, metadata
            )
            pb_request = datatransfer.EnrollDataSourcesRequest.pb(request)
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

    class _GetDataSource(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("GetDataSource")

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
            request: datatransfer.GetDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.DataSource:
            r"""Call the get data source method over HTTP.

            Args:
                request (~.datatransfer.GetDataSourceRequest):
                    The request object. A request to get data source info.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datatransfer.DataSource:
                    Defines the properties and custom
                parameters for a data source.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dataSources/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/dataSources/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_data_source(request, metadata)
            pb_request = datatransfer.GetDataSourceRequest.pb(request)
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
            resp = datatransfer.DataSource()
            pb_resp = datatransfer.DataSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_source(resp)
            return resp

    class _GetTransferConfig(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("GetTransferConfig")

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
            request: datatransfer.GetTransferConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer.TransferConfig:
            r"""Call the get transfer config method over HTTP.

            Args:
                request (~.datatransfer.GetTransferConfigRequest):
                    The request object. A request to get data transfer
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer.TransferConfig:
                    Represents a data transfer configuration. A transfer
                configuration contains all metadata needed to perform a
                data transfer. For example, ``destination_dataset_id``
                specifies where data should be stored. When a new
                transfer configuration is created, the specified
                ``destination_dataset_id`` is created when needed and
                shared with the appropriate data source service account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/transferConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/transferConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_transfer_config(
                request, metadata
            )
            pb_request = datatransfer.GetTransferConfigRequest.pb(request)
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
            resp = transfer.TransferConfig()
            pb_resp = transfer.TransferConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_transfer_config(resp)
            return resp

    class _GetTransferRun(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("GetTransferRun")

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
            request: datatransfer.GetTransferRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer.TransferRun:
            r"""Call the get transfer run method over HTTP.

            Args:
                request (~.datatransfer.GetTransferRunRequest):
                    The request object. A request to get data transfer run
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer.TransferRun:
                    Represents a data transfer run.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/transferConfigs/*/runs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/transferConfigs/*/runs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_transfer_run(
                request, metadata
            )
            pb_request = datatransfer.GetTransferRunRequest.pb(request)
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
            resp = transfer.TransferRun()
            pb_resp = transfer.TransferRun.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_transfer_run(resp)
            return resp

    class _ListDataSources(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("ListDataSources")

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
            request: datatransfer.ListDataSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.ListDataSourcesResponse:
            r"""Call the list data sources method over HTTP.

            Args:
                request (~.datatransfer.ListDataSourcesRequest):
                    The request object. Request to list supported data
                sources and their data transfer
                settings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datatransfer.ListDataSourcesResponse:
                    Returns list of supported data
                sources and their metadata.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/dataSources",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/dataSources",
                },
            ]
            request, metadata = self._interceptor.pre_list_data_sources(
                request, metadata
            )
            pb_request = datatransfer.ListDataSourcesRequest.pb(request)
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
            resp = datatransfer.ListDataSourcesResponse()
            pb_resp = datatransfer.ListDataSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_data_sources(resp)
            return resp

    class _ListTransferConfigs(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("ListTransferConfigs")

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
            request: datatransfer.ListTransferConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.ListTransferConfigsResponse:
            r"""Call the list transfer configs method over HTTP.

            Args:
                request (~.datatransfer.ListTransferConfigsRequest):
                    The request object. A request to list data transfers
                configured for a BigQuery project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datatransfer.ListTransferConfigsResponse:
                    The returned list of pipelines in the
                project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/transferConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/transferConfigs",
                },
            ]
            request, metadata = self._interceptor.pre_list_transfer_configs(
                request, metadata
            )
            pb_request = datatransfer.ListTransferConfigsRequest.pb(request)
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
            resp = datatransfer.ListTransferConfigsResponse()
            pb_resp = datatransfer.ListTransferConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_transfer_configs(resp)
            return resp

    class _ListTransferLogs(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("ListTransferLogs")

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
            request: datatransfer.ListTransferLogsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.ListTransferLogsResponse:
            r"""Call the list transfer logs method over HTTP.

            Args:
                request (~.datatransfer.ListTransferLogsRequest):
                    The request object. A request to get user facing log
                messages associated with data transfer
                run.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datatransfer.ListTransferLogsResponse:
                    The returned list transfer run
                messages.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/transferConfigs/*/runs/*}/transferLogs",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/transferConfigs/*/runs/*}/transferLogs",
                },
            ]
            request, metadata = self._interceptor.pre_list_transfer_logs(
                request, metadata
            )
            pb_request = datatransfer.ListTransferLogsRequest.pb(request)
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
            resp = datatransfer.ListTransferLogsResponse()
            pb_resp = datatransfer.ListTransferLogsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_transfer_logs(resp)
            return resp

    class _ListTransferRuns(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("ListTransferRuns")

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
            request: datatransfer.ListTransferRunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.ListTransferRunsResponse:
            r"""Call the list transfer runs method over HTTP.

            Args:
                request (~.datatransfer.ListTransferRunsRequest):
                    The request object. A request to list data transfer runs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datatransfer.ListTransferRunsResponse:
                    The returned list of pipelines in the
                project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/transferConfigs/*}/runs",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/transferConfigs/*}/runs",
                },
            ]
            request, metadata = self._interceptor.pre_list_transfer_runs(
                request, metadata
            )
            pb_request = datatransfer.ListTransferRunsRequest.pb(request)
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
            resp = datatransfer.ListTransferRunsResponse()
            pb_resp = datatransfer.ListTransferRunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_transfer_runs(resp)
            return resp

    class _ScheduleTransferRuns(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("ScheduleTransferRuns")

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
            request: datatransfer.ScheduleTransferRunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.ScheduleTransferRunsResponse:
            r"""Call the schedule transfer runs method over HTTP.

            Args:
                request (~.datatransfer.ScheduleTransferRunsRequest):
                    The request object. A request to schedule transfer runs
                for a time range.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datatransfer.ScheduleTransferRunsResponse:
                    A response to schedule transfer runs
                for a time range.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/transferConfigs/*}:scheduleRuns",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/transferConfigs/*}:scheduleRuns",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_schedule_transfer_runs(
                request, metadata
            )
            pb_request = datatransfer.ScheduleTransferRunsRequest.pb(request)
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
            resp = datatransfer.ScheduleTransferRunsResponse()
            pb_resp = datatransfer.ScheduleTransferRunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_schedule_transfer_runs(resp)
            return resp

    class _StartManualTransferRuns(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("StartManualTransferRuns")

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
            request: datatransfer.StartManualTransferRunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datatransfer.StartManualTransferRunsResponse:
            r"""Call the start manual transfer
            runs method over HTTP.

                Args:
                    request (~.datatransfer.StartManualTransferRunsRequest):
                        The request object. A request to start manual transfer
                    runs.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.datatransfer.StartManualTransferRunsResponse:
                        A response to start manual transfer
                    runs.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/transferConfigs/*}:startManualRuns",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/transferConfigs/*}:startManualRuns",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_start_manual_transfer_runs(
                request, metadata
            )
            pb_request = datatransfer.StartManualTransferRunsRequest.pb(request)
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
            resp = datatransfer.StartManualTransferRunsResponse()
            pb_resp = datatransfer.StartManualTransferRunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_start_manual_transfer_runs(resp)
            return resp

    class _UnenrollDataSources(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("UnenrollDataSources")

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
            request: datatransfer.UnenrollDataSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the unenroll data sources method over HTTP.

            Args:
                request (~.datatransfer.UnenrollDataSourcesRequest):
                    The request object. A request to unenroll a set of data sources so they are
                no longer visible in the BigQuery UI's ``Transfer`` tab.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*}:unenrollDataSources",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_unenroll_data_sources(
                request, metadata
            )
            pb_request = datatransfer.UnenrollDataSourcesRequest.pb(request)
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

    class _UpdateTransferConfig(DataTransferServiceRestStub):
        def __hash__(self):
            return hash("UpdateTransferConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: datatransfer.UpdateTransferConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer.TransferConfig:
            r"""Call the update transfer config method over HTTP.

            Args:
                request (~.datatransfer.UpdateTransferConfigRequest):
                    The request object. A request to update a transfer
                configuration. To update the user id of
                the transfer configuration,
                authorization info needs to be provided.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer.TransferConfig:
                    Represents a data transfer configuration. A transfer
                configuration contains all metadata needed to perform a
                data transfer. For example, ``destination_dataset_id``
                specifies where data should be stored. When a new
                transfer configuration is created, the specified
                ``destination_dataset_id`` is created when needed and
                shared with the appropriate data source service account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{transfer_config.name=projects/*/locations/*/transferConfigs/*}",
                    "body": "transfer_config",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{transfer_config.name=projects/*/transferConfigs/*}",
                    "body": "transfer_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_transfer_config(
                request, metadata
            )
            pb_request = datatransfer.UpdateTransferConfigRequest.pb(request)
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
            resp = transfer.TransferConfig()
            pb_resp = transfer.TransferConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_transfer_config(resp)
            return resp

    @property
    def check_valid_creds(
        self,
    ) -> Callable[
        [datatransfer.CheckValidCredsRequest], datatransfer.CheckValidCredsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckValidCreds(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_transfer_config(
        self,
    ) -> Callable[[datatransfer.CreateTransferConfigRequest], transfer.TransferConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTransferConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_transfer_config(
        self,
    ) -> Callable[[datatransfer.DeleteTransferConfigRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTransferConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_transfer_run(
        self,
    ) -> Callable[[datatransfer.DeleteTransferRunRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTransferRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enroll_data_sources(
        self,
    ) -> Callable[[datatransfer.EnrollDataSourcesRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnrollDataSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_source(
        self,
    ) -> Callable[[datatransfer.GetDataSourceRequest], datatransfer.DataSource]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_transfer_config(
        self,
    ) -> Callable[[datatransfer.GetTransferConfigRequest], transfer.TransferConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTransferConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_transfer_run(
        self,
    ) -> Callable[[datatransfer.GetTransferRunRequest], transfer.TransferRun]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTransferRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_data_sources(
        self,
    ) -> Callable[
        [datatransfer.ListDataSourcesRequest], datatransfer.ListDataSourcesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDataSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_transfer_configs(
        self,
    ) -> Callable[
        [datatransfer.ListTransferConfigsRequest],
        datatransfer.ListTransferConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTransferConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_transfer_logs(
        self,
    ) -> Callable[
        [datatransfer.ListTransferLogsRequest], datatransfer.ListTransferLogsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTransferLogs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_transfer_runs(
        self,
    ) -> Callable[
        [datatransfer.ListTransferRunsRequest], datatransfer.ListTransferRunsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTransferRuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def schedule_transfer_runs(
        self,
    ) -> Callable[
        [datatransfer.ScheduleTransferRunsRequest],
        datatransfer.ScheduleTransferRunsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ScheduleTransferRuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_manual_transfer_runs(
        self,
    ) -> Callable[
        [datatransfer.StartManualTransferRunsRequest],
        datatransfer.StartManualTransferRunsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartManualTransferRuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def unenroll_data_sources(
        self,
    ) -> Callable[[datatransfer.UnenrollDataSourcesRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UnenrollDataSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_transfer_config(
        self,
    ) -> Callable[[datatransfer.UpdateTransferConfigRequest], transfer.TransferConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTransferConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(DataTransferServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
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

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(DataTransferServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
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

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DataTransferServiceRestTransport",)
