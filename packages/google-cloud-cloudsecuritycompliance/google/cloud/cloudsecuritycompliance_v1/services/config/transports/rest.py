# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import google.protobuf
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.cloudsecuritycompliance_v1.types import common, config

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseConfigRestTransport

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

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class ConfigRestInterceptor:
    """Interceptor for Config.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ConfigRestTransport.

    .. code-block:: python
        class MyCustomConfigInterceptor(ConfigRestInterceptor):
            def pre_create_cloud_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cloud_control(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_framework(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_framework(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cloud_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_framework(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_cloud_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cloud_control(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_framework(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_framework(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_cloud_controls(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_cloud_controls(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_frameworks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_frameworks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cloud_control(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cloud_control(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_framework(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_framework(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ConfigRestTransport(interceptor=MyCustomConfigInterceptor())
        client = ConfigClient(transport=transport)


    """

    def pre_create_cloud_control(
        self,
        request: config.CreateCloudControlRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        config.CreateCloudControlRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_cloud_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_create_cloud_control(
        self, response: common.CloudControl
    ) -> common.CloudControl:
        """Post-rpc interceptor for create_cloud_control

        DEPRECATED. Please use the `post_create_cloud_control_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_create_cloud_control` interceptor runs
        before the `post_create_cloud_control_with_metadata` interceptor.
        """
        return response

    def post_create_cloud_control_with_metadata(
        self,
        response: common.CloudControl,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[common.CloudControl, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_cloud_control

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_create_cloud_control_with_metadata`
        interceptor in new development instead of the `post_create_cloud_control` interceptor.
        When both interceptors are used, this `post_create_cloud_control_with_metadata` interceptor runs after the
        `post_create_cloud_control` interceptor. The (possibly modified) response returned by
        `post_create_cloud_control` will be passed to
        `post_create_cloud_control_with_metadata`.
        """
        return response, metadata

    def pre_create_framework(
        self,
        request: config.CreateFrameworkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[config.CreateFrameworkRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_framework

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_create_framework(self, response: common.Framework) -> common.Framework:
        """Post-rpc interceptor for create_framework

        DEPRECATED. Please use the `post_create_framework_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_create_framework` interceptor runs
        before the `post_create_framework_with_metadata` interceptor.
        """
        return response

    def post_create_framework_with_metadata(
        self,
        response: common.Framework,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[common.Framework, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_framework

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_create_framework_with_metadata`
        interceptor in new development instead of the `post_create_framework` interceptor.
        When both interceptors are used, this `post_create_framework_with_metadata` interceptor runs after the
        `post_create_framework` interceptor. The (possibly modified) response returned by
        `post_create_framework` will be passed to
        `post_create_framework_with_metadata`.
        """
        return response, metadata

    def pre_delete_cloud_control(
        self,
        request: config.DeleteCloudControlRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        config.DeleteCloudControlRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_cloud_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def pre_delete_framework(
        self,
        request: config.DeleteFrameworkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[config.DeleteFrameworkRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_framework

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def pre_get_cloud_control(
        self,
        request: config.GetCloudControlRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[config.GetCloudControlRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_cloud_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_get_cloud_control(
        self, response: common.CloudControl
    ) -> common.CloudControl:
        """Post-rpc interceptor for get_cloud_control

        DEPRECATED. Please use the `post_get_cloud_control_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_get_cloud_control` interceptor runs
        before the `post_get_cloud_control_with_metadata` interceptor.
        """
        return response

    def post_get_cloud_control_with_metadata(
        self,
        response: common.CloudControl,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[common.CloudControl, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_cloud_control

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_get_cloud_control_with_metadata`
        interceptor in new development instead of the `post_get_cloud_control` interceptor.
        When both interceptors are used, this `post_get_cloud_control_with_metadata` interceptor runs after the
        `post_get_cloud_control` interceptor. The (possibly modified) response returned by
        `post_get_cloud_control` will be passed to
        `post_get_cloud_control_with_metadata`.
        """
        return response, metadata

    def pre_get_framework(
        self,
        request: config.GetFrameworkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[config.GetFrameworkRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_framework

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_get_framework(self, response: common.Framework) -> common.Framework:
        """Post-rpc interceptor for get_framework

        DEPRECATED. Please use the `post_get_framework_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_get_framework` interceptor runs
        before the `post_get_framework_with_metadata` interceptor.
        """
        return response

    def post_get_framework_with_metadata(
        self,
        response: common.Framework,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[common.Framework, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_framework

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_get_framework_with_metadata`
        interceptor in new development instead of the `post_get_framework` interceptor.
        When both interceptors are used, this `post_get_framework_with_metadata` interceptor runs after the
        `post_get_framework` interceptor. The (possibly modified) response returned by
        `post_get_framework` will be passed to
        `post_get_framework_with_metadata`.
        """
        return response, metadata

    def pre_list_cloud_controls(
        self,
        request: config.ListCloudControlsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        config.ListCloudControlsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_cloud_controls

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_list_cloud_controls(
        self, response: config.ListCloudControlsResponse
    ) -> config.ListCloudControlsResponse:
        """Post-rpc interceptor for list_cloud_controls

        DEPRECATED. Please use the `post_list_cloud_controls_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_list_cloud_controls` interceptor runs
        before the `post_list_cloud_controls_with_metadata` interceptor.
        """
        return response

    def post_list_cloud_controls_with_metadata(
        self,
        response: config.ListCloudControlsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        config.ListCloudControlsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_cloud_controls

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_list_cloud_controls_with_metadata`
        interceptor in new development instead of the `post_list_cloud_controls` interceptor.
        When both interceptors are used, this `post_list_cloud_controls_with_metadata` interceptor runs after the
        `post_list_cloud_controls` interceptor. The (possibly modified) response returned by
        `post_list_cloud_controls` will be passed to
        `post_list_cloud_controls_with_metadata`.
        """
        return response, metadata

    def pre_list_frameworks(
        self,
        request: config.ListFrameworksRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[config.ListFrameworksRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_frameworks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_list_frameworks(
        self, response: config.ListFrameworksResponse
    ) -> config.ListFrameworksResponse:
        """Post-rpc interceptor for list_frameworks

        DEPRECATED. Please use the `post_list_frameworks_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_list_frameworks` interceptor runs
        before the `post_list_frameworks_with_metadata` interceptor.
        """
        return response

    def post_list_frameworks_with_metadata(
        self,
        response: config.ListFrameworksResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[config.ListFrameworksResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_frameworks

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_list_frameworks_with_metadata`
        interceptor in new development instead of the `post_list_frameworks` interceptor.
        When both interceptors are used, this `post_list_frameworks_with_metadata` interceptor runs after the
        `post_list_frameworks` interceptor. The (possibly modified) response returned by
        `post_list_frameworks` will be passed to
        `post_list_frameworks_with_metadata`.
        """
        return response, metadata

    def pre_update_cloud_control(
        self,
        request: config.UpdateCloudControlRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        config.UpdateCloudControlRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_cloud_control

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_update_cloud_control(
        self, response: common.CloudControl
    ) -> common.CloudControl:
        """Post-rpc interceptor for update_cloud_control

        DEPRECATED. Please use the `post_update_cloud_control_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_update_cloud_control` interceptor runs
        before the `post_update_cloud_control_with_metadata` interceptor.
        """
        return response

    def post_update_cloud_control_with_metadata(
        self,
        response: common.CloudControl,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[common.CloudControl, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_cloud_control

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_update_cloud_control_with_metadata`
        interceptor in new development instead of the `post_update_cloud_control` interceptor.
        When both interceptors are used, this `post_update_cloud_control_with_metadata` interceptor runs after the
        `post_update_cloud_control` interceptor. The (possibly modified) response returned by
        `post_update_cloud_control` will be passed to
        `post_update_cloud_control_with_metadata`.
        """
        return response, metadata

    def pre_update_framework(
        self,
        request: config.UpdateFrameworkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[config.UpdateFrameworkRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_framework

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_update_framework(self, response: common.Framework) -> common.Framework:
        """Post-rpc interceptor for update_framework

        DEPRECATED. Please use the `post_update_framework_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Config server but before
        it is returned to user code. This `post_update_framework` interceptor runs
        before the `post_update_framework_with_metadata` interceptor.
        """
        return response

    def post_update_framework_with_metadata(
        self,
        response: common.Framework,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[common.Framework, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_framework

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Config server but before it is returned to user code.

        We recommend only using this `post_update_framework_with_metadata`
        interceptor in new development instead of the `post_update_framework` interceptor.
        When both interceptors are used, this `post_update_framework_with_metadata` interceptor runs after the
        `post_update_framework` interceptor. The (possibly modified) response returned by
        `post_update_framework` will be passed to
        `post_update_framework_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Config server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Config server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Config server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Config server but before
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
        before they are sent to the Config server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Config server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Config server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Config server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ConfigRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ConfigRestInterceptor


class ConfigRestTransport(_BaseConfigRestTransport):
    """REST backend synchronous transport for Config.

    Config Service manages compliance frameworks, cloud controls,
    and their configurations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudsecuritycompliance.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ConfigRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudsecuritycompliance.googleapis.com').
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
        self._interceptor = interceptor or ConfigRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateCloudControl(
        _BaseConfigRestTransport._BaseCreateCloudControl, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.CreateCloudControl")

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
            request: config.CreateCloudControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> common.CloudControl:
            r"""Call the create cloud control method over HTTP.

            Args:
                request (~.config.CreateCloudControlRequest):
                    The request object. Request message for creating a
                CloudControl
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.common.CloudControl:
                    A CloudControl is the fundamental unit encapsulating the
                rules to meet a specific security or compliance intent.
                It can contain various rule types (like Organization
                Policies, CEL expressions, etc.) enabling different
                enforcement modes (Preventive, Detective, Audit).
                CloudControls are often parameterized for reusability
                and can be either BUILT_IN (provided by Google) or
                CUSTOM (defined by the user).

            """

            http_options = (
                _BaseConfigRestTransport._BaseCreateCloudControl._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_cloud_control(
                request, metadata
            )
            transcoded_request = _BaseConfigRestTransport._BaseCreateCloudControl._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseConfigRestTransport._BaseCreateCloudControl._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseCreateCloudControl._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.CreateCloudControl",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "CreateCloudControl",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._CreateCloudControl._get_response(
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
            resp = common.CloudControl()
            pb_resp = common.CloudControl.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_cloud_control(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_cloud_control_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = common.CloudControl.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.create_cloud_control",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "CreateCloudControl",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateFramework(
        _BaseConfigRestTransport._BaseCreateFramework, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.CreateFramework")

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
            request: config.CreateFrameworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> common.Framework:
            r"""Call the create framework method over HTTP.

            Args:
                request (~.config.CreateFrameworkRequest):
                    The request object. Request message for creating a
                Framework
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.common.Framework:
                    A Framework is a collection of
                CloudControls to address security and
                compliance requirements. Frameworks can
                be used for prevention, detection, and
                auditing. They can be either built-in,
                industry-standard frameworks provided by
                GCP/AZURE/AWS (e.g., NIST, FedRAMP) or
                custom frameworks created by users.

            """

            http_options = (
                _BaseConfigRestTransport._BaseCreateFramework._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_framework(
                request, metadata
            )
            transcoded_request = (
                _BaseConfigRestTransport._BaseCreateFramework._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseConfigRestTransport._BaseCreateFramework._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseCreateFramework._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.CreateFramework",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "CreateFramework",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._CreateFramework._get_response(
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
            resp = common.Framework()
            pb_resp = common.Framework.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_framework(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_framework_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = common.Framework.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.create_framework",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "CreateFramework",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteCloudControl(
        _BaseConfigRestTransport._BaseDeleteCloudControl, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.DeleteCloudControl")

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
            request: config.DeleteCloudControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete cloud control method over HTTP.

            Args:
                request (~.config.DeleteCloudControlRequest):
                    The request object. Request message for deleting a
                CloudControl.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseConfigRestTransport._BaseDeleteCloudControl._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_cloud_control(
                request, metadata
            )
            transcoded_request = _BaseConfigRestTransport._BaseDeleteCloudControl._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseDeleteCloudControl._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.DeleteCloudControl",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "DeleteCloudControl",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._DeleteCloudControl._get_response(
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

    class _DeleteFramework(
        _BaseConfigRestTransport._BaseDeleteFramework, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.DeleteFramework")

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
            request: config.DeleteFrameworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete framework method over HTTP.

            Args:
                request (~.config.DeleteFrameworkRequest):
                    The request object. Request message for deleting a
                Framework.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseConfigRestTransport._BaseDeleteFramework._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_framework(
                request, metadata
            )
            transcoded_request = (
                _BaseConfigRestTransport._BaseDeleteFramework._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseDeleteFramework._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.DeleteFramework",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "DeleteFramework",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._DeleteFramework._get_response(
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

    class _GetCloudControl(
        _BaseConfigRestTransport._BaseGetCloudControl, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.GetCloudControl")

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
            request: config.GetCloudControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> common.CloudControl:
            r"""Call the get cloud control method over HTTP.

            Args:
                request (~.config.GetCloudControlRequest):
                    The request object. Request message for getting a
                CloudControl.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.common.CloudControl:
                    A CloudControl is the fundamental unit encapsulating the
                rules to meet a specific security or compliance intent.
                It can contain various rule types (like Organization
                Policies, CEL expressions, etc.) enabling different
                enforcement modes (Preventive, Detective, Audit).
                CloudControls are often parameterized for reusability
                and can be either BUILT_IN (provided by Google) or
                CUSTOM (defined by the user).

            """

            http_options = (
                _BaseConfigRestTransport._BaseGetCloudControl._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_cloud_control(
                request, metadata
            )
            transcoded_request = (
                _BaseConfigRestTransport._BaseGetCloudControl._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseGetCloudControl._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.GetCloudControl",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetCloudControl",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._GetCloudControl._get_response(
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
            resp = common.CloudControl()
            pb_resp = common.CloudControl.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_cloud_control(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_cloud_control_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = common.CloudControl.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.get_cloud_control",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetCloudControl",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetFramework(_BaseConfigRestTransport._BaseGetFramework, ConfigRestStub):
        def __hash__(self):
            return hash("ConfigRestTransport.GetFramework")

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
            request: config.GetFrameworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> common.Framework:
            r"""Call the get framework method over HTTP.

            Args:
                request (~.config.GetFrameworkRequest):
                    The request object. Request message for getting a
                Framework.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.common.Framework:
                    A Framework is a collection of
                CloudControls to address security and
                compliance requirements. Frameworks can
                be used for prevention, detection, and
                auditing. They can be either built-in,
                industry-standard frameworks provided by
                GCP/AZURE/AWS (e.g., NIST, FedRAMP) or
                custom frameworks created by users.

            """

            http_options = (
                _BaseConfigRestTransport._BaseGetFramework._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_framework(request, metadata)
            transcoded_request = (
                _BaseConfigRestTransport._BaseGetFramework._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseGetFramework._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.GetFramework",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetFramework",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._GetFramework._get_response(
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
            resp = common.Framework()
            pb_resp = common.Framework.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_framework(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_framework_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = common.Framework.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.get_framework",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetFramework",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListCloudControls(
        _BaseConfigRestTransport._BaseListCloudControls, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.ListCloudControls")

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
            request: config.ListCloudControlsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> config.ListCloudControlsResponse:
            r"""Call the list cloud controls method over HTTP.

            Args:
                request (~.config.ListCloudControlsRequest):
                    The request object. Request message for listing
                CloudControls.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.config.ListCloudControlsResponse:
                    Response message for
                ListCloudControls.

            """

            http_options = (
                _BaseConfigRestTransport._BaseListCloudControls._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_cloud_controls(
                request, metadata
            )
            transcoded_request = (
                _BaseConfigRestTransport._BaseListCloudControls._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseListCloudControls._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.ListCloudControls",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListCloudControls",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._ListCloudControls._get_response(
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
            resp = config.ListCloudControlsResponse()
            pb_resp = config.ListCloudControlsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_cloud_controls(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_cloud_controls_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = config.ListCloudControlsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.list_cloud_controls",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListCloudControls",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListFrameworks(_BaseConfigRestTransport._BaseListFrameworks, ConfigRestStub):
        def __hash__(self):
            return hash("ConfigRestTransport.ListFrameworks")

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
            request: config.ListFrameworksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> config.ListFrameworksResponse:
            r"""Call the list frameworks method over HTTP.

            Args:
                request (~.config.ListFrameworksRequest):
                    The request object. Request message for listing
                Frameworks.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.config.ListFrameworksResponse:
                    Response message for listing
                Frameworks. Contains a paginated list of
                Framework resources.

            """

            http_options = (
                _BaseConfigRestTransport._BaseListFrameworks._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_frameworks(request, metadata)
            transcoded_request = (
                _BaseConfigRestTransport._BaseListFrameworks._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseListFrameworks._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.ListFrameworks",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListFrameworks",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._ListFrameworks._get_response(
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
            resp = config.ListFrameworksResponse()
            pb_resp = config.ListFrameworksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_frameworks(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_frameworks_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = config.ListFrameworksResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.list_frameworks",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListFrameworks",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateCloudControl(
        _BaseConfigRestTransport._BaseUpdateCloudControl, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.UpdateCloudControl")

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
            request: config.UpdateCloudControlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> common.CloudControl:
            r"""Call the update cloud control method over HTTP.

            Args:
                request (~.config.UpdateCloudControlRequest):
                    The request object. Request message for
                UpdateCloudControl.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.common.CloudControl:
                    A CloudControl is the fundamental unit encapsulating the
                rules to meet a specific security or compliance intent.
                It can contain various rule types (like Organization
                Policies, CEL expressions, etc.) enabling different
                enforcement modes (Preventive, Detective, Audit).
                CloudControls are often parameterized for reusability
                and can be either BUILT_IN (provided by Google) or
                CUSTOM (defined by the user).

            """

            http_options = (
                _BaseConfigRestTransport._BaseUpdateCloudControl._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_cloud_control(
                request, metadata
            )
            transcoded_request = _BaseConfigRestTransport._BaseUpdateCloudControl._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseConfigRestTransport._BaseUpdateCloudControl._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseUpdateCloudControl._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.UpdateCloudControl",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "UpdateCloudControl",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._UpdateCloudControl._get_response(
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
            resp = common.CloudControl()
            pb_resp = common.CloudControl.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_cloud_control(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_cloud_control_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = common.CloudControl.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.update_cloud_control",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "UpdateCloudControl",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateFramework(
        _BaseConfigRestTransport._BaseUpdateFramework, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.UpdateFramework")

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
            request: config.UpdateFrameworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> common.Framework:
            r"""Call the update framework method over HTTP.

            Args:
                request (~.config.UpdateFrameworkRequest):
                    The request object. Request message for updating a
                Framework.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.common.Framework:
                    A Framework is a collection of
                CloudControls to address security and
                compliance requirements. Frameworks can
                be used for prevention, detection, and
                auditing. They can be either built-in,
                industry-standard frameworks provided by
                GCP/AZURE/AWS (e.g., NIST, FedRAMP) or
                custom frameworks created by users.

            """

            http_options = (
                _BaseConfigRestTransport._BaseUpdateFramework._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_framework(
                request, metadata
            )
            transcoded_request = (
                _BaseConfigRestTransport._BaseUpdateFramework._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseConfigRestTransport._BaseUpdateFramework._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseUpdateFramework._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.UpdateFramework",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "UpdateFramework",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._UpdateFramework._get_response(
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
            resp = common.Framework()
            pb_resp = common.Framework.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_framework(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_framework_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = common.Framework.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigClient.update_framework",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "UpdateFramework",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_cloud_control(
        self,
    ) -> Callable[[config.CreateCloudControlRequest], common.CloudControl]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCloudControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_framework(
        self,
    ) -> Callable[[config.CreateFrameworkRequest], common.Framework]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFramework(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cloud_control(
        self,
    ) -> Callable[[config.DeleteCloudControlRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCloudControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_framework(
        self,
    ) -> Callable[[config.DeleteFrameworkRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteFramework(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cloud_control(
        self,
    ) -> Callable[[config.GetCloudControlRequest], common.CloudControl]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCloudControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_framework(self) -> Callable[[config.GetFrameworkRequest], common.Framework]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFramework(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_cloud_controls(
        self,
    ) -> Callable[[config.ListCloudControlsRequest], config.ListCloudControlsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCloudControls(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_frameworks(
        self,
    ) -> Callable[[config.ListFrameworksRequest], config.ListFrameworksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFrameworks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cloud_control(
        self,
    ) -> Callable[[config.UpdateCloudControlRequest], common.CloudControl]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCloudControl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_framework(
        self,
    ) -> Callable[[config.UpdateFrameworkRequest], common.Framework]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateFramework(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseConfigRestTransport._BaseGetLocation, ConfigRestStub):
        def __hash__(self):
            return hash("ConfigRestTransport.GetLocation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = _BaseConfigRestTransport._BaseGetLocation._get_http_options()

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseConfigRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseGetLocation._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._GetLocation._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(_BaseConfigRestTransport._BaseListLocations, ConfigRestStub):
        def __hash__(self):
            return hash("ConfigRestTransport.ListLocations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseConfigRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseConfigRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseListLocations._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._ListLocations._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseConfigRestTransport._BaseCancelOperation, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseConfigRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseConfigRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseConfigRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseCancelOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseConfigRestTransport._BaseDeleteOperation, ConfigRestStub
    ):
        def __hash__(self):
            return hash("ConfigRestTransport.DeleteOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseConfigRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseConfigRestTransport._BaseDeleteOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseDeleteOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._DeleteOperation._get_response(
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

    class _GetOperation(_BaseConfigRestTransport._BaseGetOperation, ConfigRestStub):
        def __hash__(self):
            return hash("ConfigRestTransport.GetOperation")

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
                _BaseConfigRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseConfigRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._GetOperation._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(_BaseConfigRestTransport._BaseListOperations, ConfigRestStub):
        def __hash__(self):
            return hash("ConfigRestTransport.ListOperations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseConfigRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseConfigRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseConfigRestTransport._BaseListOperations._get_query_params_json(
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
                    f"Sending request for google.cloud.cloudsecuritycompliance_v1.ConfigClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ConfigRestTransport._ListOperations._get_response(
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
                    "Received response for google.cloud.cloudsecuritycompliance_v1.ConfigAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.cloudsecuritycompliance.v1.Config",
                        "rpcName": "ListOperations",
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


__all__ = ("ConfigRestTransport",)
