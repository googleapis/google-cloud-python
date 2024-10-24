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
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.compute_v1.types import compute

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseInstanceGroupManagersRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class InstanceGroupManagersRestInterceptor:
    """Interceptor for InstanceGroupManagers.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the InstanceGroupManagersRestTransport.

    .. code-block:: python
        class MyCustomInstanceGroupManagersInterceptor(InstanceGroupManagersRestInterceptor):
            def pre_abandon_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_abandon_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_aggregated_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(self, response):
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

        transport = InstanceGroupManagersRestTransport(interceptor=MyCustomInstanceGroupManagersInterceptor())
        client = InstanceGroupManagersClient(transport=transport)


    """

    def pre_abandon_instances(
        self,
        request: compute.AbandonInstancesInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AbandonInstancesInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for abandon_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_abandon_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for abandon_instances

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_aggregated_list(
        self,
        request: compute.AggregatedListInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AggregatedListInstanceGroupManagersRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_aggregated_list(
        self, response: compute.InstanceGroupManagerAggregatedList
    ) -> compute.InstanceGroupManagerAggregatedList:
        """Post-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_apply_updates_to_instances(
        self,
        request: compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for apply_updates_to_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_apply_updates_to_instances(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for apply_updates_to_instances

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_create_instances(
        self,
        request: compute.CreateInstancesInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.CreateInstancesInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_create_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for create_instances

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeleteInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DeleteInstanceGroupManagerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_delete_instances(
        self,
        request: compute.DeleteInstancesInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.DeleteInstancesInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_delete_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete_instances

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_delete_per_instance_configs(
        self,
        request: compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_delete_per_instance_configs(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for delete_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetInstanceGroupManagerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_get(
        self, response: compute.InstanceGroupManager
    ) -> compute.InstanceGroupManager:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.InsertInstanceGroupManagerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListInstanceGroupManagersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_list(
        self, response: compute.InstanceGroupManagerList
    ) -> compute.InstanceGroupManagerList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list_errors(
        self,
        request: compute.ListErrorsInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListErrorsInstanceGroupManagersRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_errors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_list_errors(
        self, response: compute.InstanceGroupManagersListErrorsResponse
    ) -> compute.InstanceGroupManagersListErrorsResponse:
        """Post-rpc interceptor for list_errors

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list_managed_instances(
        self,
        request: compute.ListManagedInstancesInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListManagedInstancesInstanceGroupManagersRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_managed_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_list_managed_instances(
        self, response: compute.InstanceGroupManagersListManagedInstancesResponse
    ) -> compute.InstanceGroupManagersListManagedInstancesResponse:
        """Post-rpc interceptor for list_managed_instances

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_list_per_instance_configs(
        self,
        request: compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_list_per_instance_configs(
        self, response: compute.InstanceGroupManagersListPerInstanceConfigsResp
    ) -> compute.InstanceGroupManagersListPerInstanceConfigsResp:
        """Post-rpc interceptor for list_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchInstanceGroupManagerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_patch_per_instance_configs(
        self,
        request: compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for patch_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_patch_per_instance_configs(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for patch_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_recreate_instances(
        self,
        request: compute.RecreateInstancesInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.RecreateInstancesInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for recreate_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_recreate_instances(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for recreate_instances

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_resize(
        self,
        request: compute.ResizeInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ResizeInstanceGroupManagerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for resize

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_resize(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for resize

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_set_instance_template(
        self,
        request: compute.SetInstanceTemplateInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetInstanceTemplateInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for set_instance_template

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_set_instance_template(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_instance_template

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_set_target_pools(
        self,
        request: compute.SetTargetPoolsInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetTargetPoolsInstanceGroupManagerRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_target_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_set_target_pools(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_target_pools

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response

    def pre_update_per_instance_configs(
        self,
        request: compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_per_instance_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InstanceGroupManagers server.
        """
        return request, metadata

    def post_update_per_instance_configs(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for update_per_instance_configs

        Override in a subclass to manipulate the response
        after it is returned by the InstanceGroupManagers server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class InstanceGroupManagersRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: InstanceGroupManagersRestInterceptor


class InstanceGroupManagersRestTransport(_BaseInstanceGroupManagersRestTransport):
    """REST backend synchronous transport for InstanceGroupManagers.

    The InstanceGroupManagers API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
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
        interceptor: Optional[InstanceGroupManagersRestInterceptor] = None,
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
        self._interceptor = interceptor or InstanceGroupManagersRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AbandonInstances(
        _BaseInstanceGroupManagersRestTransport._BaseAbandonInstances,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.AbandonInstances")

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
            request: compute.AbandonInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the abandon instances method over HTTP.

            Args:
                request (~.compute.AbandonInstancesInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.AbandonInstances.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseAbandonInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_abandon_instances(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseAbandonInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseAbandonInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseAbandonInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                InstanceGroupManagersRestTransport._AbandonInstances._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
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

    class _AggregatedList(
        _BaseInstanceGroupManagersRestTransport._BaseAggregatedList,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.AggregatedList")

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
            request: compute.AggregatedListInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceGroupManagerAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListInstanceGroupManagersRequest):
                    The request object. A request message for
                InstanceGroupManagers.AggregatedList.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceGroupManagerAggregatedList:

            """

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseAggregatedList._get_http_options()
            )
            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseAggregatedList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseAggregatedList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._AggregatedList._get_response(
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
            resp = compute.InstanceGroupManagerAggregatedList()
            pb_resp = compute.InstanceGroupManagerAggregatedList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregated_list(resp)
            return resp

    class _ApplyUpdatesToInstances(
        _BaseInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.ApplyUpdatesToInstances")

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
            request: compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the apply updates to
            instances method over HTTP.

                Args:
                    request (~.compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest):
                        The request object. A request message for
                    InstanceGroupManagers.ApplyUpdatesToInstances.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_apply_updates_to_instances(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._ApplyUpdatesToInstances._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_apply_updates_to_instances(resp)
            return resp

    class _CreateInstances(
        _BaseInstanceGroupManagersRestTransport._BaseCreateInstances,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.CreateInstances")

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
            request: compute.CreateInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the create instances method over HTTP.

            Args:
                request (~.compute.CreateInstancesInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.CreateInstances.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseCreateInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_instances(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseCreateInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseCreateInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseCreateInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                InstanceGroupManagersRestTransport._CreateInstances._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
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

    class _Delete(
        _BaseInstanceGroupManagersRestTransport._BaseDelete,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.Delete")

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
            request: compute.DeleteInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.Delete. See the
                method description for details.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseDelete._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseDelete._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._Delete._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete(resp)
            return resp

    class _DeleteInstances(
        _BaseInstanceGroupManagersRestTransport._BaseDeleteInstances,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.DeleteInstances")

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
            request: compute.DeleteInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete instances method over HTTP.

            Args:
                request (~.compute.DeleteInstancesInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.DeleteInstances.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseDeleteInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_instances(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseDeleteInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseDeleteInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseDeleteInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                InstanceGroupManagersRestTransport._DeleteInstances._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
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

    class _DeletePerInstanceConfigs(
        _BaseInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.DeletePerInstanceConfigs")

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
            request: compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete per instance
            configs method over HTTP.

                Args:
                    request (~.compute.DeletePerInstanceConfigsInstanceGroupManagerRequest):
                        The request object. A request message for
                    InstanceGroupManagers.DeletePerInstanceConfigs.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._DeletePerInstanceConfigs._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_per_instance_configs(resp)
            return resp

    class _Get(
        _BaseInstanceGroupManagersRestTransport._BaseGet, InstanceGroupManagersRestStub
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.Get")

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
            request: compute.GetInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceGroupManager:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.Get. See the
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseGet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseInstanceGroupManagersRestTransport._BaseGet._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._Get._get_response(
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
            resp = compute.InstanceGroupManager()
            pb_resp = compute.InstanceGroupManager.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(
        _BaseInstanceGroupManagersRestTransport._BaseInsert,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.Insert")

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
            request: compute.InsertInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.Insert. See the
                method description for details.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseInsert._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseInsert._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._Insert._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_insert(resp)
            return resp

    class _List(
        _BaseInstanceGroupManagersRestTransport._BaseList, InstanceGroupManagersRestStub
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.List")

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
            request: compute.ListInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceGroupManagerList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListInstanceGroupManagersRequest):
                    The request object. A request message for
                InstanceGroupManagers.List. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceGroupManagerList:
                    [Output Only] A list of managed instance groups.
            """

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._List._get_response(
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
            resp = compute.InstanceGroupManagerList()
            pb_resp = compute.InstanceGroupManagerList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _ListErrors(
        _BaseInstanceGroupManagersRestTransport._BaseListErrors,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.ListErrors")

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
            request: compute.ListErrorsInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceGroupManagersListErrorsResponse:
            r"""Call the list errors method over HTTP.

            Args:
                request (~.compute.ListErrorsInstanceGroupManagersRequest):
                    The request object. A request message for
                InstanceGroupManagers.ListErrors. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceGroupManagersListErrorsResponse:

            """

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseListErrors._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_errors(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseListErrors._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseListErrors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._ListErrors._get_response(
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
            resp = compute.InstanceGroupManagersListErrorsResponse()
            pb_resp = compute.InstanceGroupManagersListErrorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_errors(resp)
            return resp

    class _ListManagedInstances(
        _BaseInstanceGroupManagersRestTransport._BaseListManagedInstances,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.ListManagedInstances")

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
            request: compute.ListManagedInstancesInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceGroupManagersListManagedInstancesResponse:
            r"""Call the list managed instances method over HTTP.

            Args:
                request (~.compute.ListManagedInstancesInstanceGroupManagersRequest):
                    The request object. A request message for
                InstanceGroupManagers.ListManagedInstances.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceGroupManagersListManagedInstancesResponse:

            """

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseListManagedInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_managed_instances(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseListManagedInstances._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseListManagedInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                InstanceGroupManagersRestTransport._ListManagedInstances._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InstanceGroupManagersListManagedInstancesResponse()
            pb_resp = compute.InstanceGroupManagersListManagedInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_managed_instances(resp)
            return resp

    class _ListPerInstanceConfigs(
        _BaseInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.ListPerInstanceConfigs")

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
            request: compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceGroupManagersListPerInstanceConfigsResp:
            r"""Call the list per instance configs method over HTTP.

            Args:
                request (~.compute.ListPerInstanceConfigsInstanceGroupManagersRequest):
                    The request object. A request message for
                InstanceGroupManagers.ListPerInstanceConfigs.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceGroupManagersListPerInstanceConfigsResp:

            """

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._ListPerInstanceConfigs._get_response(
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
            resp = compute.InstanceGroupManagersListPerInstanceConfigsResp()
            pb_resp = compute.InstanceGroupManagersListPerInstanceConfigsResp.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_per_instance_configs(resp)
            return resp

    class _Patch(
        _BaseInstanceGroupManagersRestTransport._BasePatch,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.Patch")

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
            request: compute.PatchInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.Patch. See the
                method description for details.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BasePatch._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BasePatch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BasePatch._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._Patch._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_patch(resp)
            return resp

    class _PatchPerInstanceConfigs(
        _BaseInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.PatchPerInstanceConfigs")

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
            request: compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch per instance
            configs method over HTTP.

                Args:
                    request (~.compute.PatchPerInstanceConfigsInstanceGroupManagerRequest):
                        The request object. A request message for
                    InstanceGroupManagers.PatchPerInstanceConfigs.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._PatchPerInstanceConfigs._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_patch_per_instance_configs(resp)
            return resp

    class _RecreateInstances(
        _BaseInstanceGroupManagersRestTransport._BaseRecreateInstances,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.RecreateInstances")

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
            request: compute.RecreateInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the recreate instances method over HTTP.

            Args:
                request (~.compute.RecreateInstancesInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.RecreateInstances.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseRecreateInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_recreate_instances(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseRecreateInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseRecreateInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseRecreateInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                InstanceGroupManagersRestTransport._RecreateInstances._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
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

    class _Resize(
        _BaseInstanceGroupManagersRestTransport._BaseResize,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.Resize")

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
            request: compute.ResizeInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the resize method over HTTP.

            Args:
                request (~.compute.ResizeInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.Resize. See the
                method description for details.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseResize._get_http_options()
            )
            request, metadata = self._interceptor.pre_resize(request, metadata)
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseResize._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseResize._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._Resize._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_resize(resp)
            return resp

    class _SetInstanceTemplate(
        _BaseInstanceGroupManagersRestTransport._BaseSetInstanceTemplate,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.SetInstanceTemplate")

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
            request: compute.SetInstanceTemplateInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set instance template method over HTTP.

            Args:
                request (~.compute.SetInstanceTemplateInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.SetInstanceTemplate.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_instance_template(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                InstanceGroupManagersRestTransport._SetInstanceTemplate._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
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

    class _SetTargetPools(
        _BaseInstanceGroupManagersRestTransport._BaseSetTargetPools,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.SetTargetPools")

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
            request: compute.SetTargetPoolsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set target pools method over HTTP.

            Args:
                request (~.compute.SetTargetPoolsInstanceGroupManagerRequest):
                    The request object. A request message for
                InstanceGroupManagers.SetTargetPools.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseSetTargetPools._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_target_pools(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseSetTargetPools._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseSetTargetPools._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseSetTargetPools._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._SetTargetPools._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_target_pools(resp)
            return resp

    class _UpdatePerInstanceConfigs(
        _BaseInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs,
        InstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("InstanceGroupManagersRestTransport.UpdatePerInstanceConfigs")

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
            request: compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update per instance
            configs method over HTTP.

                Args:
                    request (~.compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest):
                        The request object. A request message for
                    InstanceGroupManagers.UpdatePerInstanceConfigs.
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

            http_options = (
                _BaseInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            body = _BaseInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = InstanceGroupManagersRestTransport._UpdatePerInstanceConfigs._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_per_instance_configs(resp)
            return resp

    @property
    def abandon_instances(
        self,
    ) -> Callable[
        [compute.AbandonInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AbandonInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListInstanceGroupManagersRequest],
        compute.InstanceGroupManagerAggregatedList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def apply_updates_to_instances(
        self,
    ) -> Callable[
        [compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApplyUpdatesToInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_instances(
        self,
    ) -> Callable[
        [compute.CreateInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_instances(
        self,
    ) -> Callable[
        [compute.DeleteInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_per_instance_configs(
        self,
    ) -> Callable[
        [compute.DeletePerInstanceConfigsInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetInstanceGroupManagerRequest], compute.InstanceGroupManager
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListInstanceGroupManagersRequest], compute.InstanceGroupManagerList
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_errors(
        self,
    ) -> Callable[
        [compute.ListErrorsInstanceGroupManagersRequest],
        compute.InstanceGroupManagersListErrorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListErrors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_managed_instances(
        self,
    ) -> Callable[
        [compute.ListManagedInstancesInstanceGroupManagersRequest],
        compute.InstanceGroupManagersListManagedInstancesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListManagedInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_per_instance_configs(
        self,
    ) -> Callable[
        [compute.ListPerInstanceConfigsInstanceGroupManagersRequest],
        compute.InstanceGroupManagersListPerInstanceConfigsResp,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_per_instance_configs(
        self,
    ) -> Callable[
        [compute.PatchPerInstanceConfigsInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchPerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def recreate_instances(
        self,
    ) -> Callable[
        [compute.RecreateInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RecreateInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resize(
        self,
    ) -> Callable[[compute.ResizeInstanceGroupManagerRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Resize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_instance_template(
        self,
    ) -> Callable[
        [compute.SetInstanceTemplateInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetInstanceTemplate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_target_pools(
        self,
    ) -> Callable[
        [compute.SetTargetPoolsInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetTargetPools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_per_instance_configs(
        self,
    ) -> Callable[
        [compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePerInstanceConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("InstanceGroupManagersRestTransport",)
