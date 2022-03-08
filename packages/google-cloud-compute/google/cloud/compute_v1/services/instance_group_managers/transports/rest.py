# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from requests import __version__ as requests_version
import dataclasses
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.compute_v1.types import compute

from .base import (
    InstanceGroupManagersTransport,
    DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO,
)


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
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
            def pre_abandon_instances(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_abandon_instances(response):
                logging.log(f"Received response: {response}")

            def pre_aggregated_list(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(response):
                logging.log(f"Received response: {response}")

            def pre_apply_updates_to_instances(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_apply_updates_to_instances(response):
                logging.log(f"Received response: {response}")

            def pre_create_instances(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_instances(response):
                logging.log(f"Received response: {response}")

            def pre_delete(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(response):
                logging.log(f"Received response: {response}")

            def pre_delete_instances(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_instances(response):
                logging.log(f"Received response: {response}")

            def pre_delete_per_instance_configs(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_per_instance_configs(response):
                logging.log(f"Received response: {response}")

            def pre_get(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(response):
                logging.log(f"Received response: {response}")

            def pre_insert(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert(response):
                logging.log(f"Received response: {response}")

            def pre_list(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(response):
                logging.log(f"Received response: {response}")

            def pre_list_errors(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_errors(response):
                logging.log(f"Received response: {response}")

            def pre_list_managed_instances(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_managed_instances(response):
                logging.log(f"Received response: {response}")

            def pre_list_per_instance_configs(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_per_instance_configs(response):
                logging.log(f"Received response: {response}")

            def pre_patch(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch(response):
                logging.log(f"Received response: {response}")

            def pre_patch_per_instance_configs(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch_per_instance_configs(response):
                logging.log(f"Received response: {response}")

            def pre_recreate_instances(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_recreate_instances(response):
                logging.log(f"Received response: {response}")

            def pre_resize(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resize(response):
                logging.log(f"Received response: {response}")

            def pre_set_instance_template(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_instance_template(response):
                logging.log(f"Received response: {response}")

            def pre_set_target_pools(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_target_pools(response):
                logging.log(f"Received response: {response}")

            def pre_update_per_instance_configs(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_per_instance_configs(response):
                logging.log(f"Received response: {response}")

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


class InstanceGroupManagersRestTransport(InstanceGroupManagersTransport):
    """REST backend transport for InstanceGroupManagers.

    The InstanceGroupManagers API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    _STUBS: Dict[str, InstanceGroupManagersRestStub] = {}

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[InstanceGroupManagersRestInterceptor] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or InstanceGroupManagersRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AbandonInstances(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("AbandonInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.AbandonInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the abandon instances method over HTTP.

            Args:
                request (~.compute.AbandonInstancesInstanceGroupManagerRequest):
                    The request object. Messages
                A request message for
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/abandonInstances",
                    "body": "instance_group_managers_abandon_instances_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_abandon_instances(
                request, metadata
            )
            request_kwargs = compute.AbandonInstancesInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersAbandonInstancesRequest.to_json(
                compute.InstanceGroupManagersAbandonInstancesRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.AbandonInstancesInstanceGroupManagerRequest.to_json(
                    compute.AbandonInstancesInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_abandon_instances(resp)
            return resp

    class _AggregatedList(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("AggregatedList")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.AggregatedListInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/aggregated/instanceGroupManagers",
                },
            ]
            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            request_kwargs = compute.AggregatedListInstanceGroupManagersRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.AggregatedListInstanceGroupManagersRequest.to_json(
                    compute.AggregatedListInstanceGroupManagersRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InstanceGroupManagerAggregatedList.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_aggregated_list(resp)
            return resp

    class _ApplyUpdatesToInstances(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ApplyUpdatesToInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/applyUpdatesToInstances",
                    "body": "instance_group_managers_apply_updates_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_apply_updates_to_instances(
                request, metadata
            )
            request_kwargs = compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersApplyUpdatesRequest.to_json(
                compute.InstanceGroupManagersApplyUpdatesRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest.to_json(
                    compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_apply_updates_to_instances(resp)
            return resp

    class _CreateInstances(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("CreateInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.CreateInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/createInstances",
                    "body": "instance_group_managers_create_instances_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_create_instances(
                request, metadata
            )
            request_kwargs = compute.CreateInstancesInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersCreateInstancesRequest.to_json(
                compute.InstanceGroupManagersCreateInstancesRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.CreateInstancesInstanceGroupManagerRequest.to_json(
                    compute.CreateInstancesInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_create_instances(resp)
            return resp

    class _Delete(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Delete")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.DeleteInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}",
                },
            ]
            request, metadata = self._interceptor.pre_delete(request, metadata)
            request_kwargs = compute.DeleteInstanceGroupManagerRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.DeleteInstanceGroupManagerRequest.to_json(
                    compute.DeleteInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_delete(resp)
            return resp

    class _DeleteInstances(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("DeleteInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.DeleteInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/deleteInstances",
                    "body": "instance_group_managers_delete_instances_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_delete_instances(
                request, metadata
            )
            request_kwargs = compute.DeleteInstancesInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersDeleteInstancesRequest.to_json(
                compute.InstanceGroupManagersDeleteInstancesRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.DeleteInstancesInstanceGroupManagerRequest.to_json(
                    compute.DeleteInstancesInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_delete_instances(resp)
            return resp

    class _DeletePerInstanceConfigs(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("DeletePerInstanceConfigs")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.DeletePerInstanceConfigsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/deletePerInstanceConfigs",
                    "body": "instance_group_managers_delete_per_instance_configs_req_resource",
                },
            ]
            request, metadata = self._interceptor.pre_delete_per_instance_configs(
                request, metadata
            )
            request_kwargs = compute.DeletePerInstanceConfigsInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersDeletePerInstanceConfigsReq.to_json(
                compute.InstanceGroupManagersDeletePerInstanceConfigsReq(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.DeletePerInstanceConfigsInstanceGroupManagerRequest.to_json(
                    compute.DeletePerInstanceConfigsInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_delete_per_instance_configs(resp)
            return resp

    class _Get(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Get")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}",
                },
            ]
            request, metadata = self._interceptor.pre_get(request, metadata)
            request_kwargs = compute.GetInstanceGroupManagerRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetInstanceGroupManagerRequest.to_json(
                    compute.GetInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InstanceGroupManager.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Insert")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.InsertInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers",
                    "body": "instance_group_manager_resource",
                },
            ]
            request, metadata = self._interceptor.pre_insert(request, metadata)
            request_kwargs = compute.InsertInstanceGroupManagerRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManager.to_json(
                compute.InstanceGroupManager(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.InsertInstanceGroupManagerRequest.to_json(
                    compute.InsertInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_insert(resp)
            return resp

    class _List(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("List")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ListInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers",
                },
            ]
            request, metadata = self._interceptor.pre_list(request, metadata)
            request_kwargs = compute.ListInstanceGroupManagersRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ListInstanceGroupManagersRequest.to_json(
                    compute.ListInstanceGroupManagersRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InstanceGroupManagerList.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list(resp)
            return resp

    class _ListErrors(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ListErrors")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ListErrorsInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/listErrors",
                },
            ]
            request, metadata = self._interceptor.pre_list_errors(request, metadata)
            request_kwargs = compute.ListErrorsInstanceGroupManagersRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ListErrorsInstanceGroupManagersRequest.to_json(
                    compute.ListErrorsInstanceGroupManagersRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InstanceGroupManagersListErrorsResponse.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list_errors(resp)
            return resp

    class _ListManagedInstances(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ListManagedInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ListManagedInstancesInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/listManagedInstances",
                },
            ]
            request, metadata = self._interceptor.pre_list_managed_instances(
                request, metadata
            )
            request_kwargs = compute.ListManagedInstancesInstanceGroupManagersRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ListManagedInstancesInstanceGroupManagersRequest.to_json(
                    compute.ListManagedInstancesInstanceGroupManagersRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InstanceGroupManagersListManagedInstancesResponse.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list_managed_instances(resp)
            return resp

    class _ListPerInstanceConfigs(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("ListPerInstanceConfigs")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ListPerInstanceConfigsInstanceGroupManagersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/listPerInstanceConfigs",
                },
            ]
            request, metadata = self._interceptor.pre_list_per_instance_configs(
                request, metadata
            )
            request_kwargs = compute.ListPerInstanceConfigsInstanceGroupManagersRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ListPerInstanceConfigsInstanceGroupManagersRequest.to_json(
                    compute.ListPerInstanceConfigsInstanceGroupManagersRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InstanceGroupManagersListPerInstanceConfigsResp.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_list_per_instance_configs(resp)
            return resp

    class _Patch(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Patch")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.PatchInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}",
                    "body": "instance_group_manager_resource",
                },
            ]
            request, metadata = self._interceptor.pre_patch(request, metadata)
            request_kwargs = compute.PatchInstanceGroupManagerRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManager.to_json(
                compute.InstanceGroupManager(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.PatchInstanceGroupManagerRequest.to_json(
                    compute.PatchInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_patch(resp)
            return resp

    class _PatchPerInstanceConfigs(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("PatchPerInstanceConfigs")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.PatchPerInstanceConfigsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/patchPerInstanceConfigs",
                    "body": "instance_group_managers_patch_per_instance_configs_req_resource",
                },
            ]
            request, metadata = self._interceptor.pre_patch_per_instance_configs(
                request, metadata
            )
            request_kwargs = compute.PatchPerInstanceConfigsInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersPatchPerInstanceConfigsReq.to_json(
                compute.InstanceGroupManagersPatchPerInstanceConfigsReq(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.PatchPerInstanceConfigsInstanceGroupManagerRequest.to_json(
                    compute.PatchPerInstanceConfigsInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_patch_per_instance_configs(resp)
            return resp

    class _RecreateInstances(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("RecreateInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.RecreateInstancesInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/recreateInstances",
                    "body": "instance_group_managers_recreate_instances_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_recreate_instances(
                request, metadata
            )
            request_kwargs = compute.RecreateInstancesInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersRecreateInstancesRequest.to_json(
                compute.InstanceGroupManagersRecreateInstancesRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.RecreateInstancesInstanceGroupManagerRequest.to_json(
                    compute.RecreateInstancesInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_recreate_instances(resp)
            return resp

    class _Resize(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("Resize")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
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
            request: compute.ResizeInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/resize",
                },
            ]
            request, metadata = self._interceptor.pre_resize(request, metadata)
            request_kwargs = compute.ResizeInstanceGroupManagerRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ResizeInstanceGroupManagerRequest.to_json(
                    compute.ResizeInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_resize(resp)
            return resp

    class _SetInstanceTemplate(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("SetInstanceTemplate")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetInstanceTemplateInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/setInstanceTemplate",
                    "body": "instance_group_managers_set_instance_template_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_instance_template(
                request, metadata
            )
            request_kwargs = compute.SetInstanceTemplateInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersSetInstanceTemplateRequest.to_json(
                compute.InstanceGroupManagersSetInstanceTemplateRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetInstanceTemplateInstanceGroupManagerRequest.to_json(
                    compute.SetInstanceTemplateInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_set_instance_template(resp)
            return resp

    class _SetTargetPools(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("SetTargetPools")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetTargetPoolsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/setTargetPools",
                    "body": "instance_group_managers_set_target_pools_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_target_pools(
                request, metadata
            )
            request_kwargs = compute.SetTargetPoolsInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersSetTargetPoolsRequest.to_json(
                compute.InstanceGroupManagersSetTargetPoolsRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetTargetPoolsInstanceGroupManagerRequest.to_json(
                    compute.SetTargetPoolsInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_set_target_pools(resp)
            return resp

    class _UpdatePerInstanceConfigs(InstanceGroupManagersRestStub):
        def __hash__(self):
            return hash("UpdatePerInstanceConfigs")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
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
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{instance_group_manager}/updatePerInstanceConfigs",
                    "body": "instance_group_managers_update_per_instance_configs_req_resource",
                },
            ]
            request, metadata = self._interceptor.pre_update_per_instance_configs(
                request, metadata
            )
            request_kwargs = compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstanceGroupManagersUpdatePerInstanceConfigsReq.to_json(
                compute.InstanceGroupManagersUpdatePerInstanceConfigsReq(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest.to_json(
                    compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
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
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )
            resp = self._interceptor.post_update_per_instance_configs(resp)
            return resp

    @property
    def abandon_instances(
        self,
    ) -> Callable[
        [compute.AbandonInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("abandon_instances")
        if not stub:
            stub = self._STUBS["abandon_instances"] = self._AbandonInstances(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListInstanceGroupManagersRequest],
        compute.InstanceGroupManagerAggregatedList,
    ]:
        stub = self._STUBS.get("aggregated_list")
        if not stub:
            stub = self._STUBS["aggregated_list"] = self._AggregatedList(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def apply_updates_to_instances(
        self,
    ) -> Callable[
        [compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("apply_updates_to_instances")
        if not stub:
            stub = self._STUBS[
                "apply_updates_to_instances"
            ] = self._ApplyUpdatesToInstances(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def create_instances(
        self,
    ) -> Callable[
        [compute.CreateInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("create_instances")
        if not stub:
            stub = self._STUBS["create_instances"] = self._CreateInstances(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteInstanceGroupManagerRequest], compute.Operation]:
        stub = self._STUBS.get("delete")
        if not stub:
            stub = self._STUBS["delete"] = self._Delete(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def delete_instances(
        self,
    ) -> Callable[
        [compute.DeleteInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("delete_instances")
        if not stub:
            stub = self._STUBS["delete_instances"] = self._DeleteInstances(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def delete_per_instance_configs(
        self,
    ) -> Callable[
        [compute.DeletePerInstanceConfigsInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("delete_per_instance_configs")
        if not stub:
            stub = self._STUBS[
                "delete_per_instance_configs"
            ] = self._DeletePerInstanceConfigs(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetInstanceGroupManagerRequest], compute.InstanceGroupManager
    ]:
        stub = self._STUBS.get("get")
        if not stub:
            stub = self._STUBS["get"] = self._Get(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertInstanceGroupManagerRequest], compute.Operation]:
        stub = self._STUBS.get("insert")
        if not stub:
            stub = self._STUBS["insert"] = self._Insert(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListInstanceGroupManagersRequest], compute.InstanceGroupManagerList
    ]:
        stub = self._STUBS.get("list")
        if not stub:
            stub = self._STUBS["list"] = self._List(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def list_errors(
        self,
    ) -> Callable[
        [compute.ListErrorsInstanceGroupManagersRequest],
        compute.InstanceGroupManagersListErrorsResponse,
    ]:
        stub = self._STUBS.get("list_errors")
        if not stub:
            stub = self._STUBS["list_errors"] = self._ListErrors(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def list_managed_instances(
        self,
    ) -> Callable[
        [compute.ListManagedInstancesInstanceGroupManagersRequest],
        compute.InstanceGroupManagersListManagedInstancesResponse,
    ]:
        stub = self._STUBS.get("list_managed_instances")
        if not stub:
            stub = self._STUBS["list_managed_instances"] = self._ListManagedInstances(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def list_per_instance_configs(
        self,
    ) -> Callable[
        [compute.ListPerInstanceConfigsInstanceGroupManagersRequest],
        compute.InstanceGroupManagersListPerInstanceConfigsResp,
    ]:
        stub = self._STUBS.get("list_per_instance_configs")
        if not stub:
            stub = self._STUBS[
                "list_per_instance_configs"
            ] = self._ListPerInstanceConfigs(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchInstanceGroupManagerRequest], compute.Operation]:
        stub = self._STUBS.get("patch")
        if not stub:
            stub = self._STUBS["patch"] = self._Patch(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def patch_per_instance_configs(
        self,
    ) -> Callable[
        [compute.PatchPerInstanceConfigsInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("patch_per_instance_configs")
        if not stub:
            stub = self._STUBS[
                "patch_per_instance_configs"
            ] = self._PatchPerInstanceConfigs(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def recreate_instances(
        self,
    ) -> Callable[
        [compute.RecreateInstancesInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("recreate_instances")
        if not stub:
            stub = self._STUBS["recreate_instances"] = self._RecreateInstances(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def resize(
        self,
    ) -> Callable[[compute.ResizeInstanceGroupManagerRequest], compute.Operation]:
        stub = self._STUBS.get("resize")
        if not stub:
            stub = self._STUBS["resize"] = self._Resize(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def set_instance_template(
        self,
    ) -> Callable[
        [compute.SetInstanceTemplateInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("set_instance_template")
        if not stub:
            stub = self._STUBS["set_instance_template"] = self._SetInstanceTemplate(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def set_target_pools(
        self,
    ) -> Callable[
        [compute.SetTargetPoolsInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("set_target_pools")
        if not stub:
            stub = self._STUBS["set_target_pools"] = self._SetTargetPools(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    @property
    def update_per_instance_configs(
        self,
    ) -> Callable[
        [compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest], compute.Operation
    ]:
        stub = self._STUBS.get("update_per_instance_configs")
        if not stub:
            stub = self._STUBS[
                "update_per_instance_configs"
            ] = self._UpdatePerInstanceConfigs(
                self._session, self._host, self._interceptor
            )

        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return stub  # type: ignore

    def close(self):
        self._session.close()


__all__ = ("InstanceGroupManagersRestTransport",)
