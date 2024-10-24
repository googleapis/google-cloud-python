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
from .rest_base import _BaseRegionInstanceGroupManagersRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
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


class RegionInstanceGroupManagersRestTransport(
    _BaseRegionInstanceGroupManagersRestTransport
):
    """REST backend synchronous transport for RegionInstanceGroupManagers.

    The RegionInstanceGroupManagers API.

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
        self._interceptor = interceptor or RegionInstanceGroupManagersRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AbandonInstances(
        _BaseRegionInstanceGroupManagersRestTransport._BaseAbandonInstances,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.AbandonInstances")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseAbandonInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_abandon_instances(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseAbandonInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseAbandonInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseAbandonInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._AbandonInstances._get_response(
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
            resp = self._interceptor.post_abandon_instances(resp)
            return resp

    class _ApplyUpdatesToInstances(
        _BaseRegionInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash(
                "RegionInstanceGroupManagersRestTransport.ApplyUpdatesToInstances"
            )

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_apply_updates_to_instances(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseApplyUpdatesToInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._ApplyUpdatesToInstances._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseCreateInstances,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.CreateInstances")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseCreateInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_instances(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseCreateInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseCreateInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseCreateInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionInstanceGroupManagersRestTransport._CreateInstances._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseDelete,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.Delete")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseDelete._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseDelete._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._Delete._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseDeleteInstances,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.DeleteInstances")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseDeleteInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_instances(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseDeleteInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseDeleteInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseDeleteInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionInstanceGroupManagersRestTransport._DeleteInstances._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash(
                "RegionInstanceGroupManagersRestTransport.DeletePerInstanceConfigs"
            )

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseDeletePerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._DeletePerInstanceConfigs._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseGet,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.Get")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseGet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseGet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._Get._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseInsert,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.Insert")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseInsert._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseInsert._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._Insert._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseList,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.List")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._List._get_response(
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
            resp = compute.RegionInstanceGroupManagerList()
            pb_resp = compute.RegionInstanceGroupManagerList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _ListErrors(
        _BaseRegionInstanceGroupManagersRestTransport._BaseListErrors,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.ListErrors")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseListErrors._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_errors(request, metadata)
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseListErrors._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseListErrors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionInstanceGroupManagersRestTransport._ListErrors._get_response(
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
            resp = compute.RegionInstanceGroupManagersListErrorsResponse()
            pb_resp = compute.RegionInstanceGroupManagersListErrorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_errors(resp)
            return resp

    class _ListManagedInstances(
        _BaseRegionInstanceGroupManagersRestTransport._BaseListManagedInstances,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.ListManagedInstances")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseListManagedInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_managed_instances(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseListManagedInstances._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseListManagedInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._ListManagedInstances._get_response(
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
            resp = compute.RegionInstanceGroupManagersListInstancesResponse()
            pb_resp = compute.RegionInstanceGroupManagersListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_managed_instances(resp)
            return resp

    class _ListPerInstanceConfigs(
        _BaseRegionInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash(
                "RegionInstanceGroupManagersRestTransport.ListPerInstanceConfigs"
            )

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseListPerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._ListPerInstanceConfigs._get_response(
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
            resp = compute.RegionInstanceGroupManagersListInstanceConfigsResp()
            pb_resp = compute.RegionInstanceGroupManagersListInstanceConfigsResp.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_per_instance_configs(resp)
            return resp

    class _Patch(
        _BaseRegionInstanceGroupManagersRestTransport._BasePatch,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.Patch")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BasePatch._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BasePatch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BasePatch._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._Patch._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash(
                "RegionInstanceGroupManagersRestTransport.PatchPerInstanceConfigs"
            )

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BasePatchPerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._PatchPerInstanceConfigs._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseRecreateInstances,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.RecreateInstances")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseRecreateInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_recreate_instances(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseRecreateInstances._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseRecreateInstances._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseRecreateInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._RecreateInstances._get_response(
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
            resp = self._interceptor.post_recreate_instances(resp)
            return resp

    class _Resize(
        _BaseRegionInstanceGroupManagersRestTransport._BaseResize,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.Resize")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseResize._get_http_options()
            )
            request, metadata = self._interceptor.pre_resize(request, metadata)
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseResize._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseResize._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._Resize._get_response(
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
        _BaseRegionInstanceGroupManagersRestTransport._BaseSetInstanceTemplate,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.SetInstanceTemplate")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_instance_template(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseSetInstanceTemplate._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._SetInstanceTemplate._get_response(
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
            resp = self._interceptor.post_set_instance_template(resp)
            return resp

    class _SetTargetPools(
        _BaseRegionInstanceGroupManagersRestTransport._BaseSetTargetPools,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash("RegionInstanceGroupManagersRestTransport.SetTargetPools")

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseSetTargetPools._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_target_pools(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseSetTargetPools._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseSetTargetPools._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseSetTargetPools._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                RegionInstanceGroupManagersRestTransport._SetTargetPools._get_response(
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
            resp = self._interceptor.post_set_target_pools(resp)
            return resp

    class _UpdatePerInstanceConfigs(
        _BaseRegionInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs,
        RegionInstanceGroupManagersRestStub,
    ):
        def __hash__(self):
            return hash(
                "RegionInstanceGroupManagersRestTransport.UpdatePerInstanceConfigs"
            )

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

            http_options = (
                _BaseRegionInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_per_instance_configs(
                request, metadata
            )
            transcoded_request = _BaseRegionInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionInstanceGroupManagersRestTransport._BaseUpdatePerInstanceConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RegionInstanceGroupManagersRestTransport._UpdatePerInstanceConfigs._get_response(
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
