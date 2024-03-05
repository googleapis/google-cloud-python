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


from google.cloud.compute_v1.types import compute

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import RegionInstanceGroupManagersTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RegionInstanceGroupManagersRestInterceptor:
    """Interceptor for RegionInstanceGroupManagers.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionInstanceGroupManagersRestTransport.

    .. code-block:: python
        class MyCustomRegionInstanceGroupManagersInterceptor(RegionInstanceGroupManagersRestInterceptor):
            def pre_abandon_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_abandon_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_apply_updates_to_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_apply_updates_to_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_per_instance_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_per_instance_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_errors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_errors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_managed_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_managed_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_per_instance_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_per_instance_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_patch(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_patch_per_instance_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch_per_instance_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_recreate_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_recreate_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resize(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resize(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_instance_template(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_instance_template(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_target_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_target_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_per_instance_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_per_instance_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RegionInstanceGroupManagersRestTransport(interceptor=MyCustomRegionInstanceGroupManagersInterceptor())
        client = RegionInstanceGroupManagersClient(transport=transport)


    """

    def pre_abandon_instances(
        self,
        request: compute.AbandonInstancesRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AbandonInstancesRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for abandon_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_abandon_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for abandon_instances

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_apply_updates_to_instances(
        self,
        request: compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for apply_updates_to_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_apply_updates_to_instances(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for apply_updates_to_instances

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_create_instances(
        self,
        request: compute.CreateInstancesRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.CreateInstancesRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_create_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for create_instances

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeleteRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.DeleteRegionInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_delete_instances(
        self,
        request: compute.DeleteInstancesRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.DeleteInstancesRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_delete_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete_instances

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_delete_per_instance_configs(
        self,
        request: compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_delete_per_instance_configs(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for delete_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetRegionInstanceGroupManagerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_get(
        self, response: compute.InstanceGroupManager
    ) -> compute.InstanceGroupManager:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.InsertRegionInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListRegionInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListRegionInstanceGroupManagersRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_list(
        self, response: compute.RegionInstanceGroupManagerList
    ) -> compute.RegionInstanceGroupManagerList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list_errors(
        self,
        request: compute.ListErrorsRegionInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListErrorsRegionInstanceGroupManagersRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_errors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_list_errors(
        self, response: compute.RegionInstanceGroupManagersListErrorsResponse
    ) -> compute.RegionInstanceGroupManagersListErrorsResponse:
        """Post-rpc interceptor for list_errors

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list_managed_instances(
        self,
        request: compute.ListManagedInstancesRegionInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListManagedInstancesRegionInstanceGroupManagersRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_managed_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_list_managed_instances(
        self, response: compute.RegionInstanceGroupManagersListInstancesResponse
    ) -> compute.RegionInstanceGroupManagersListInstancesResponse:
        """Post-rpc interceptor for list_managed_instances

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list_per_instance_configs(
        self,
        request: compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_list_per_instance_configs(
        self, response: compute.RegionInstanceGroupManagersListInstanceConfigsResp
    ) -> compute.RegionInstanceGroupManagersListInstanceConfigsResp:
        """Post-rpc interceptor for list_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.PatchRegionInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_patch_per_instance_configs(
        self,
        request: compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for patch_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_patch_per_instance_configs(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for patch_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_recreate_instances(
        self,
        request: compute.RecreateInstancesRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.RecreateInstancesRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for recreate_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_recreate_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for recreate_instances

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_resize(
        self,
        request: compute.ResizeRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ResizeRegionInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for resize

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_resize(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for resize

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_set_instance_template(
        self,
        request: compute.SetInstanceTemplateRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetInstanceTemplateRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for set_instance_template

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_set_instance_template(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_instance_template

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_set_target_pools(
        self,
        request: compute.SetTargetPoolsRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetTargetPoolsRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for set_target_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_set_target_pools(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_target_pools

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_update_per_instance_configs(
        self,
        request: compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionInstanceGroupManagers server.
        """
        return request, metadata

    def post_update_per_instance_configs(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for update_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the RegionInstanceGroupManagers server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionInstanceGroupManagersRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionInstanceGroupManagersRestInterceptor


class RegionInstanceGroupManagersRestTransport(RegionInstanceGroupManagersTransport):
    """REST backend transport for RegionInstanceGroupManagers.

    The RegionInstanceGroupManagers API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RegionInstanceGroupManagersRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'compute.googleapis.com').
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
        self._interceptor = interceptor or RegionInstanceGroupManagersRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AbandonInstances(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("AbandonInstances")

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
            request: compute.AbandonInstancesRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the abandon instances method over HTTP.

            Args:
                request (~.compute.AbandonInstancesRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.AbandonInstances.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/abandonInstances",
                    "body": "region_instance_group_managers_abandon_instances_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_abandon_instances(
                request, metadata
            )
            pb_request = compute.AbandonInstancesRegionInstanceGroupManagerRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_abandon_instances(resp)
            return resp

    class _ApplyUpdatesToInstances(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ApplyUpdatesToInstances")

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
            request: compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the apply updates to
            instances method over HTTP.

                Args:
                    request (~.compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest):
                        The request object. A request message for
                    RegionInstanceGroupManagers.ApplyUpdatesToInstances.
                    See the method description for details.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.compute.Operation:
                        Represents an Operation resource. Google Compute Engine
                    has three Operation resources: \*
                    `Global </compute/docs/reference/rest/v1/globalOperations>`__
                    \*
                    `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                    \*
                    `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                    You can use an operation resource to manage asynchronous
                    API requests. For more information, read Handling API
                    responses. Operations can be global, regional or zonal.
                    - For global operations, use the ``globalOperations``
                    resource. - For regional operations, use the
                    ``regionOperations`` resource. - For zonal operations,
                    use the ``zoneOperations`` resource. For more
                    information, read Global, Regional, and Zonal Resources.
                    Note that completed Operation resources have a limited
                    retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/applyUpdatesToInstances",
                    "body": "region_instance_group_managers_apply_updates_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_apply_updates_to_instances(
                request, metadata
            )
            pb_request = (
                compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_apply_updates_to_instances(resp)
            return resp

    class _CreateInstances(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("CreateInstances")

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
            request: compute.CreateInstancesRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the create instances method over HTTP.

            Args:
                request (~.compute.CreateInstancesRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.CreateInstances.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/createInstances",
                    "body": "region_instance_group_managers_create_instances_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_create_instances(
                request, metadata
            )
            pb_request = compute.CreateInstancesRegionInstanceGroupManagerRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_instances(resp)
            return resp

    class _Delete(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Delete")

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
            request: compute.DeleteRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.Delete. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}",
                },
            ]
            request, metadata = self._interceptor.pre_delete(request, metadata)
            pb_request = compute.DeleteRegionInstanceGroupManagerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete(resp)
            return resp

    class _DeleteInstances(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("DeleteInstances")

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
            request: compute.DeleteInstancesRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete instances method over HTTP.

            Args:
                request (~.compute.DeleteInstancesRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.DeleteInstances.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/deleteInstances",
                    "body": "region_instance_group_managers_delete_instances_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_delete_instances(
                request, metadata
            )
            pb_request = compute.DeleteInstancesRegionInstanceGroupManagerRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_instances(resp)
            return resp

    class _DeletePerInstanceConfigs(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("DeletePerInstanceConfigs")

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
            request: compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete per instance
            configs method over HTTP.

                Args:
                    request (~.compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest):
                        The request object. A request message for
                    RegionInstanceGroupManagers.DeletePerInstanceConfigs.
                    See the method description for details.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.compute.Operation:
                        Represents an Operation resource. Google Compute Engine
                    has three Operation resources: \*
                    `Global </compute/docs/reference/rest/v1/globalOperations>`__
                    \*
                    `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                    \*
                    `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                    You can use an operation resource to manage asynchronous
                    API requests. For more information, read Handling API
                    responses. Operations can be global, regional or zonal.
                    - For global operations, use the ``globalOperations``
                    resource. - For regional operations, use the
                    ``regionOperations`` resource. - For zonal operations,
                    use the ``zoneOperations`` resource. For more
                    information, read Global, Regional, and Zonal Resources.
                    Note that completed Operation resources have a limited
                    retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/deletePerInstanceConfigs",
                    "body": "region_instance_group_manager_delete_instance_config_req_resource",
                },
            ]
            request, metadata = self._interceptor.pre_delete_per_instance_configs(
                request, metadata
            )
            pb_request = (
                compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_per_instance_configs(resp)
            return resp

    class _Get(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Get")

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
            request: compute.GetRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceGroupManager:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.Get. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceGroupManager:
                    Represents a Managed Instance Group
                resource. An instance group is a
                collection of VM instances that you can
                manage as a single entity. For more
                information, read Instance groups. For
                zonal Managed Instance Group, use the
                instanceGroupManagers resource. For
                regional Managed Instance Group, use the
                regionInstanceGroupManagers resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}",
                },
            ]
            request, metadata = self._interceptor.pre_get(request, metadata)
            pb_request = compute.GetRegionInstanceGroupManagerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.InstanceGroupManager()
            pb_resp = compute.InstanceGroupManager.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Insert")

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
            request: compute.InsertRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.Insert. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers",
                    "body": "instance_group_manager_resource",
                },
            ]
            request, metadata = self._interceptor.pre_insert(request, metadata)
            pb_request = compute.InsertRegionInstanceGroupManagerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_insert(resp)
            return resp

    class _List(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("List")

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
            request: compute.ListRegionInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.RegionInstanceGroupManagerList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionInstanceGroupManagersRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.List. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionInstanceGroupManagerList:
                    Contains a list of managed instance
                groups.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers",
                },
            ]
            request, metadata = self._interceptor.pre_list(request, metadata)
            pb_request = compute.ListRegionInstanceGroupManagersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.RegionInstanceGroupManagerList()
            pb_resp = compute.RegionInstanceGroupManagerList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _ListErrors(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ListErrors")

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
            request: compute.ListErrorsRegionInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.RegionInstanceGroupManagersListErrorsResponse:
            r"""Call the list errors method over HTTP.

            Args:
                request (~.compute.ListErrorsRegionInstanceGroupManagersRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.ListErrors.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionInstanceGroupManagersListErrorsResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listErrors",
                },
            ]
            request, metadata = self._interceptor.pre_list_errors(request, metadata)
            pb_request = compute.ListErrorsRegionInstanceGroupManagersRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.RegionInstanceGroupManagersListErrorsResponse()
            pb_resp = compute.RegionInstanceGroupManagersListErrorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_errors(resp)
            return resp

    class _ListManagedInstances(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ListManagedInstances")

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
            request: compute.ListManagedInstancesRegionInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.RegionInstanceGroupManagersListInstancesResponse:
            r"""Call the list managed instances method over HTTP.

            Args:
                request (~.compute.ListManagedInstancesRegionInstanceGroupManagersRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.ListManagedInstances.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionInstanceGroupManagersListInstancesResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listManagedInstances",
                },
            ]
            request, metadata = self._interceptor.pre_list_managed_instances(
                request, metadata
            )
            pb_request = (
                compute.ListManagedInstancesRegionInstanceGroupManagersRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.RegionInstanceGroupManagersListInstancesResponse()
            pb_resp = compute.RegionInstanceGroupManagersListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_managed_instances(resp)
            return resp

    class _ListPerInstanceConfigs(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ListPerInstanceConfigs")

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
            request: compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.RegionInstanceGroupManagersListInstanceConfigsResp:
            r"""Call the list per instance configs method over HTTP.

            Args:
                request (~.compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.ListPerInstanceConfigs.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.RegionInstanceGroupManagersListInstanceConfigsResp:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listPerInstanceConfigs",
                },
            ]
            request, metadata = self._interceptor.pre_list_per_instance_configs(
                request, metadata
            )
            pb_request = (
                compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.RegionInstanceGroupManagersListInstanceConfigsResp()
            pb_resp = compute.RegionInstanceGroupManagersListInstanceConfigsResp.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_per_instance_configs(resp)
            return resp

    class _Patch(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Patch")

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
            request: compute.PatchRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.Patch. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}",
                    "body": "instance_group_manager_resource",
                },
            ]
            request, metadata = self._interceptor.pre_patch(request, metadata)
            pb_request = compute.PatchRegionInstanceGroupManagerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_patch(resp)
            return resp

    class _PatchPerInstanceConfigs(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("PatchPerInstanceConfigs")

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
            request: compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch per instance
            configs method over HTTP.

                Args:
                    request (~.compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest):
                        The request object. A request message for
                    RegionInstanceGroupManagers.PatchPerInstanceConfigs.
                    See the method description for details.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.compute.Operation:
                        Represents an Operation resource. Google Compute Engine
                    has three Operation resources: \*
                    `Global </compute/docs/reference/rest/v1/globalOperations>`__
                    \*
                    `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                    \*
                    `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                    You can use an operation resource to manage asynchronous
                    API requests. For more information, read Handling API
                    responses. Operations can be global, regional or zonal.
                    - For global operations, use the ``globalOperations``
                    resource. - For regional operations, use the
                    ``regionOperations`` resource. - For zonal operations,
                    use the ``zoneOperations`` resource. For more
                    information, read Global, Regional, and Zonal Resources.
                    Note that completed Operation resources have a limited
                    retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/patchPerInstanceConfigs",
                    "body": "region_instance_group_manager_patch_instance_config_req_resource",
                },
            ]
            request, metadata = self._interceptor.pre_patch_per_instance_configs(
                request, metadata
            )
            pb_request = (
                compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_patch_per_instance_configs(resp)
            return resp

    class _RecreateInstances(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("RecreateInstances")

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
            request: compute.RecreateInstancesRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the recreate instances method over HTTP.

            Args:
                request (~.compute.RecreateInstancesRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.RecreateInstances.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/recreateInstances",
                    "body": "region_instance_group_managers_recreate_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_recreate_instances(
                request, metadata
            )
            pb_request = compute.RecreateInstancesRegionInstanceGroupManagerRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_recreate_instances(resp)
            return resp

    class _Resize(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Resize")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "size": 0,
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
            request: compute.ResizeRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the resize method over HTTP.

            Args:
                request (~.compute.ResizeRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.Resize. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/resize",
                },
            ]
            request, metadata = self._interceptor.pre_resize(request, metadata)
            pb_request = compute.ResizeRegionInstanceGroupManagerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_resize(resp)
            return resp

    class _SetInstanceTemplate(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("SetInstanceTemplate")

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
            request: compute.SetInstanceTemplateRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set instance template method over HTTP.

            Args:
                request (~.compute.SetInstanceTemplateRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.SetInstanceTemplate.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/setInstanceTemplate",
                    "body": "region_instance_group_managers_set_template_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_instance_template(
                request, metadata
            )
            pb_request = (
                compute.SetInstanceTemplateRegionInstanceGroupManagerRequest.pb(request)
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_instance_template(resp)
            return resp

    class _SetTargetPools(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("SetTargetPools")

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
            request: compute.SetTargetPoolsRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set target pools method over HTTP.

            Args:
                request (~.compute.SetTargetPoolsRegionInstanceGroupManagerRequest):
                    The request object. A request message for
                RegionInstanceGroupManagers.SetTargetPools.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/setTargetPools",
                    "body": "region_instance_group_managers_set_target_pools_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_target_pools(
                request, metadata
            )
            pb_request = compute.SetTargetPoolsRegionInstanceGroupManagerRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_target_pools(resp)
            return resp

    class _UpdatePerInstanceConfigs(RegionInstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("UpdatePerInstanceConfigs")

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
            request: compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update per instance
            configs method over HTTP.

                Args:
                    request (~.compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest):
                        The request object. A request message for
                    RegionInstanceGroupManagers.UpdatePerInstanceConfigs.
                    See the method description for details.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.compute.Operation:
                        Represents an Operation resource. Google Compute Engine
                    has three Operation resources: \*
                    `Global </compute/docs/reference/rest/v1/globalOperations>`__
                    \*
                    `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                    \*
                    `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                    You can use an operation resource to manage asynchronous
                    API requests. For more information, read Handling API
                    responses. Operations can be global, regional or zonal.
                    - For global operations, use the ``globalOperations``
                    resource. - For regional operations, use the
                    ``regionOperations`` resource. - For zonal operations,
                    use the ``zoneOperations`` resource. For more
                    information, read Global, Regional, and Zonal Resources.
                    Note that completed Operation resources have a limited
                    retention period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/updatePerInstanceConfigs",
                    "body": "region_instance_group_manager_update_instance_config_req_resource",
                },
            ]
            request, metadata = self._interceptor.pre_update_per_instance_configs(
                request, metadata
            )
            pb_request = (
                compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_per_instance_configs(resp)
            return resp

    @property
    def abandon_instances(
        self,
    ) -> Callable[
        [compute.AbandonInstancesRegionInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AbandonInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def apply_updates_to_instances(
        self,
    ) -> Callable[
        [compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest],
        compute.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApplyUpdatesToInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_instances(
        self,
    ) -> Callable[
        [compute.CreateInstancesRegionInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteRegionInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_instances(
        self,
    ) -> Callable[
        [compute.DeleteInstancesRegionInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_per_instance_configs(
        self,
    ) -> Callable[
        [compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest],
        compute.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetRegionInstanceGroupManagerRequest], compute.InstanceGroupManager
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertRegionInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListRegionInstanceGroupManagersRequest],
        compute.RegionInstanceGroupManagerList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_errors(
        self,
    ) -> Callable[
        [compute.ListErrorsRegionInstanceGroupManagersRequest],
        compute.RegionInstanceGroupManagersListErrorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListErrors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_managed_instances(
        self,
    ) -> Callable[
        [compute.ListManagedInstancesRegionInstanceGroupManagersRequest],
        compute.RegionInstanceGroupManagersListInstancesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListManagedInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_per_instance_configs(
        self,
    ) -> Callable[
        [compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest],
        compute.RegionInstanceGroupManagersListInstanceConfigsResp,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchRegionInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_per_instance_configs(
        self,
    ) -> Callable[
        [compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest],
        compute.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchPerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def recreate_instances(
        self,
    ) -> Callable[
        [compute.RecreateInstancesRegionInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RecreateInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resize(
        self,
    ) -> Callable[[compute.ResizeRegionInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Resize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_instance_template(
        self,
    ) -> Callable[
        [compute.SetInstanceTemplateRegionInstanceGroupManagerRequest],
        compute.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetInstanceTemplate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_target_pools(
        self,
    ) -> Callable[
        [compute.SetTargetPoolsRegionInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetTargetPools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_per_instance_configs(
        self,
    ) -> Callable[
        [compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest],
        compute.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegionInstanceGroupManagersRestTransport",)
