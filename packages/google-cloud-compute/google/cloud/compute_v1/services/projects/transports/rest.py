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
from .base import ProjectsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ProjectsRestInterceptor:
    """Interceptor for Projects.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ProjectsRestTransport.

    .. code-block:: python
        class MyCustomProjectsInterceptor(ProjectsRestInterceptor):
            def pre_disable_xpn_host(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_xpn_host(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_xpn_resource(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_xpn_resource(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_xpn_host(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_xpn_host(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_xpn_resource(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_xpn_resource(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_xpn_host(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_xpn_host(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_xpn_resources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_xpn_resources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_xpn_hosts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_xpn_hosts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move_disk(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move_disk(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_cloud_armor_tier(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_cloud_armor_tier(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_common_instance_metadata(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_common_instance_metadata(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_default_network_tier(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_default_network_tier(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_usage_export_bucket(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_usage_export_bucket(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ProjectsRestTransport(interceptor=MyCustomProjectsInterceptor())
        client = ProjectsClient(transport=transport)


    """

    def pre_disable_xpn_host(
        self,
        request: compute.DisableXpnHostProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DisableXpnHostProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for disable_xpn_host

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_disable_xpn_host(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for disable_xpn_host

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_disable_xpn_resource(
        self,
        request: compute.DisableXpnResourceProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DisableXpnResourceProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for disable_xpn_resource

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_disable_xpn_resource(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for disable_xpn_resource

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_enable_xpn_host(
        self,
        request: compute.EnableXpnHostProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.EnableXpnHostProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for enable_xpn_host

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_enable_xpn_host(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for enable_xpn_host

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_enable_xpn_resource(
        self,
        request: compute.EnableXpnResourceProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.EnableXpnResourceProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for enable_xpn_resource

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_enable_xpn_resource(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for enable_xpn_resource

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self, request: compute.GetProjectRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[compute.GetProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_get(self, response: compute.Project) -> compute.Project:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_get_xpn_host(
        self,
        request: compute.GetXpnHostProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetXpnHostProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_xpn_host

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_get_xpn_host(self, response: compute.Project) -> compute.Project:
        """Post-rpc interceptor for get_xpn_host

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_get_xpn_resources(
        self,
        request: compute.GetXpnResourcesProjectsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetXpnResourcesProjectsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_xpn_resources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_get_xpn_resources(
        self, response: compute.ProjectsGetXpnResources
    ) -> compute.ProjectsGetXpnResources:
        """Post-rpc interceptor for get_xpn_resources

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_list_xpn_hosts(
        self,
        request: compute.ListXpnHostsProjectsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListXpnHostsProjectsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_xpn_hosts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_list_xpn_hosts(self, response: compute.XpnHostList) -> compute.XpnHostList:
        """Post-rpc interceptor for list_xpn_hosts

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_move_disk(
        self,
        request: compute.MoveDiskProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.MoveDiskProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for move_disk

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_move_disk(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for move_disk

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_move_instance(
        self,
        request: compute.MoveInstanceProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.MoveInstanceProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for move_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_move_instance(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for move_instance

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_set_cloud_armor_tier(
        self,
        request: compute.SetCloudArmorTierProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.SetCloudArmorTierProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_cloud_armor_tier

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_set_cloud_armor_tier(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_cloud_armor_tier

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_set_common_instance_metadata(
        self,
        request: compute.SetCommonInstanceMetadataProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetCommonInstanceMetadataProjectRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_common_instance_metadata

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_set_common_instance_metadata(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_common_instance_metadata

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_set_default_network_tier(
        self,
        request: compute.SetDefaultNetworkTierProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.SetDefaultNetworkTierProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_default_network_tier

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_set_default_network_tier(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_default_network_tier

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response

    def pre_set_usage_export_bucket(
        self,
        request: compute.SetUsageExportBucketProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.SetUsageExportBucketProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_usage_export_bucket

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Projects server.
        """
        return request, metadata

    def post_set_usage_export_bucket(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_usage_export_bucket

        Override in a subclass to manipulate the response
        after it is returned by the Projects server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ProjectsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ProjectsRestInterceptor


class ProjectsRestTransport(ProjectsTransport):
    """REST backend transport for Projects.

    The Projects API.

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
        interceptor: Optional[ProjectsRestInterceptor] = None,
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
        self._interceptor = interceptor or ProjectsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DisableXpnHost(ProjectsRestStub):
        def __hash__(self):
            return hash("DisableXpnHost")

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
            request: compute.DisableXpnHostProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the disable xpn host method over HTTP.

            Args:
                request (~.compute.DisableXpnHostProjectRequest):
                    The request object. A request message for
                Projects.DisableXpnHost. See the method
                description for details.
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
                    "uri": "/compute/v1/projects/{project}/disableXpnHost",
                },
            ]
            request, metadata = self._interceptor.pre_disable_xpn_host(
                request, metadata
            )
            pb_request = compute.DisableXpnHostProjectRequest.pb(request)
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
            resp = self._interceptor.post_disable_xpn_host(resp)
            return resp

    class _DisableXpnResource(ProjectsRestStub):
        def __hash__(self):
            return hash("DisableXpnResource")

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
            request: compute.DisableXpnResourceProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the disable xpn resource method over HTTP.

            Args:
                request (~.compute.DisableXpnResourceProjectRequest):
                    The request object. A request message for
                Projects.DisableXpnResource. See the
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/disableXpnResource",
                    "body": "projects_disable_xpn_resource_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_disable_xpn_resource(
                request, metadata
            )
            pb_request = compute.DisableXpnResourceProjectRequest.pb(request)
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
            resp = self._interceptor.post_disable_xpn_resource(resp)
            return resp

    class _EnableXpnHost(ProjectsRestStub):
        def __hash__(self):
            return hash("EnableXpnHost")

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
            request: compute.EnableXpnHostProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the enable xpn host method over HTTP.

            Args:
                request (~.compute.EnableXpnHostProjectRequest):
                    The request object. A request message for
                Projects.EnableXpnHost. See the method
                description for details.
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
                    "uri": "/compute/v1/projects/{project}/enableXpnHost",
                },
            ]
            request, metadata = self._interceptor.pre_enable_xpn_host(request, metadata)
            pb_request = compute.EnableXpnHostProjectRequest.pb(request)
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
            resp = self._interceptor.post_enable_xpn_host(resp)
            return resp

    class _EnableXpnResource(ProjectsRestStub):
        def __hash__(self):
            return hash("EnableXpnResource")

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
            request: compute.EnableXpnResourceProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the enable xpn resource method over HTTP.

            Args:
                request (~.compute.EnableXpnResourceProjectRequest):
                    The request object. A request message for
                Projects.EnableXpnResource. See the
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/enableXpnResource",
                    "body": "projects_enable_xpn_resource_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_enable_xpn_resource(
                request, metadata
            )
            pb_request = compute.EnableXpnResourceProjectRequest.pb(request)
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
            resp = self._interceptor.post_enable_xpn_resource(resp)
            return resp

    class _Get(ProjectsRestStub):
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
            request: compute.GetProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Project:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetProjectRequest):
                    The request object. A request message for Projects.Get.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Project:
                    Represents a Project resource. A
                project is used to organize resources in
                a Google Cloud Platform environment. For
                more information, read about the
                Resource Hierarchy.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}",
                },
            ]
            request, metadata = self._interceptor.pre_get(request, metadata)
            pb_request = compute.GetProjectRequest.pb(request)
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
            resp = compute.Project()
            pb_resp = compute.Project.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _GetXpnHost(ProjectsRestStub):
        def __hash__(self):
            return hash("GetXpnHost")

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
            request: compute.GetXpnHostProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Project:
            r"""Call the get xpn host method over HTTP.

            Args:
                request (~.compute.GetXpnHostProjectRequest):
                    The request object. A request message for
                Projects.GetXpnHost. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Project:
                    Represents a Project resource. A
                project is used to organize resources in
                a Google Cloud Platform environment. For
                more information, read about the
                Resource Hierarchy.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/getXpnHost",
                },
            ]
            request, metadata = self._interceptor.pre_get_xpn_host(request, metadata)
            pb_request = compute.GetXpnHostProjectRequest.pb(request)
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
            resp = compute.Project()
            pb_resp = compute.Project.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_xpn_host(resp)
            return resp

    class _GetXpnResources(ProjectsRestStub):
        def __hash__(self):
            return hash("GetXpnResources")

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
            request: compute.GetXpnResourcesProjectsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.ProjectsGetXpnResources:
            r"""Call the get xpn resources method over HTTP.

            Args:
                request (~.compute.GetXpnResourcesProjectsRequest):
                    The request object. A request message for
                Projects.GetXpnResources. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.ProjectsGetXpnResources:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/getXpnResources",
                },
            ]
            request, metadata = self._interceptor.pre_get_xpn_resources(
                request, metadata
            )
            pb_request = compute.GetXpnResourcesProjectsRequest.pb(request)
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
            resp = compute.ProjectsGetXpnResources()
            pb_resp = compute.ProjectsGetXpnResources.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_xpn_resources(resp)
            return resp

    class _ListXpnHosts(ProjectsRestStub):
        def __hash__(self):
            return hash("ListXpnHosts")

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
            request: compute.ListXpnHostsProjectsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.XpnHostList:
            r"""Call the list xpn hosts method over HTTP.

            Args:
                request (~.compute.ListXpnHostsProjectsRequest):
                    The request object. A request message for
                Projects.ListXpnHosts. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.XpnHostList:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/listXpnHosts",
                    "body": "projects_list_xpn_hosts_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_list_xpn_hosts(request, metadata)
            pb_request = compute.ListXpnHostsProjectsRequest.pb(request)
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
            resp = compute.XpnHostList()
            pb_resp = compute.XpnHostList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_xpn_hosts(resp)
            return resp

    class _MoveDisk(ProjectsRestStub):
        def __hash__(self):
            return hash("MoveDisk")

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
            request: compute.MoveDiskProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the move disk method over HTTP.

            Args:
                request (~.compute.MoveDiskProjectRequest):
                    The request object. A request message for
                Projects.MoveDisk. See the method
                description for details.
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
                    "uri": "/compute/v1/projects/{project}/moveDisk",
                    "body": "disk_move_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_move_disk(request, metadata)
            pb_request = compute.MoveDiskProjectRequest.pb(request)
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
            resp = self._interceptor.post_move_disk(resp)
            return resp

    class _MoveInstance(ProjectsRestStub):
        def __hash__(self):
            return hash("MoveInstance")

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
            request: compute.MoveInstanceProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the move instance method over HTTP.

            Args:
                request (~.compute.MoveInstanceProjectRequest):
                    The request object. A request message for
                Projects.MoveInstance. See the method
                description for details.
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
                    "uri": "/compute/v1/projects/{project}/moveInstance",
                    "body": "instance_move_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_move_instance(request, metadata)
            pb_request = compute.MoveInstanceProjectRequest.pb(request)
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
            resp = self._interceptor.post_move_instance(resp)
            return resp

    class _SetCloudArmorTier(ProjectsRestStub):
        def __hash__(self):
            return hash("SetCloudArmorTier")

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
            request: compute.SetCloudArmorTierProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set cloud armor tier method over HTTP.

            Args:
                request (~.compute.SetCloudArmorTierProjectRequest):
                    The request object. A request message for
                Projects.SetCloudArmorTier. See the
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/setCloudArmorTier",
                    "body": "projects_set_cloud_armor_tier_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_cloud_armor_tier(
                request, metadata
            )
            pb_request = compute.SetCloudArmorTierProjectRequest.pb(request)
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
            resp = self._interceptor.post_set_cloud_armor_tier(resp)
            return resp

    class _SetCommonInstanceMetadata(ProjectsRestStub):
        def __hash__(self):
            return hash("SetCommonInstanceMetadata")

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
            request: compute.SetCommonInstanceMetadataProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set common instance
            metadata method over HTTP.

                Args:
                    request (~.compute.SetCommonInstanceMetadataProjectRequest):
                        The request object. A request message for
                    Projects.SetCommonInstanceMetadata. See
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
                    "uri": "/compute/v1/projects/{project}/setCommonInstanceMetadata",
                    "body": "metadata_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_common_instance_metadata(
                request, metadata
            )
            pb_request = compute.SetCommonInstanceMetadataProjectRequest.pb(request)
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
            resp = self._interceptor.post_set_common_instance_metadata(resp)
            return resp

    class _SetDefaultNetworkTier(ProjectsRestStub):
        def __hash__(self):
            return hash("SetDefaultNetworkTier")

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
            request: compute.SetDefaultNetworkTierProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set default network tier method over HTTP.

            Args:
                request (~.compute.SetDefaultNetworkTierProjectRequest):
                    The request object. A request message for
                Projects.SetDefaultNetworkTier. See the
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/setDefaultNetworkTier",
                    "body": "projects_set_default_network_tier_request_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_default_network_tier(
                request, metadata
            )
            pb_request = compute.SetDefaultNetworkTierProjectRequest.pb(request)
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
            resp = self._interceptor.post_set_default_network_tier(resp)
            return resp

    class _SetUsageExportBucket(ProjectsRestStub):
        def __hash__(self):
            return hash("SetUsageExportBucket")

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
            request: compute.SetUsageExportBucketProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set usage export bucket method over HTTP.

            Args:
                request (~.compute.SetUsageExportBucketProjectRequest):
                    The request object. A request message for
                Projects.SetUsageExportBucket. See the
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/setUsageExportBucket",
                    "body": "usage_export_location_resource",
                },
            ]
            request, metadata = self._interceptor.pre_set_usage_export_bucket(
                request, metadata
            )
            pb_request = compute.SetUsageExportBucketProjectRequest.pb(request)
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
            resp = self._interceptor.post_set_usage_export_bucket(resp)
            return resp

    @property
    def disable_xpn_host(
        self,
    ) -> Callable[[compute.DisableXpnHostProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableXpnHost(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_xpn_resource(
        self,
    ) -> Callable[[compute.DisableXpnResourceProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableXpnResource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_xpn_host(
        self,
    ) -> Callable[[compute.EnableXpnHostProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableXpnHost(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_xpn_resource(
        self,
    ) -> Callable[[compute.EnableXpnResourceProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableXpnResource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(self) -> Callable[[compute.GetProjectRequest], compute.Project]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_xpn_host(
        self,
    ) -> Callable[[compute.GetXpnHostProjectRequest], compute.Project]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetXpnHost(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_xpn_resources(
        self,
    ) -> Callable[
        [compute.GetXpnResourcesProjectsRequest], compute.ProjectsGetXpnResources
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetXpnResources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_xpn_hosts(
        self,
    ) -> Callable[[compute.ListXpnHostsProjectsRequest], compute.XpnHostList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListXpnHosts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move_disk(
        self,
    ) -> Callable[[compute.MoveDiskProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MoveDisk(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move_instance(
        self,
    ) -> Callable[[compute.MoveInstanceProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MoveInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_cloud_armor_tier(
        self,
    ) -> Callable[[compute.SetCloudArmorTierProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetCloudArmorTier(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_common_instance_metadata(
        self,
    ) -> Callable[[compute.SetCommonInstanceMetadataProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetCommonInstanceMetadata(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_default_network_tier(
        self,
    ) -> Callable[[compute.SetDefaultNetworkTierProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetDefaultNetworkTier(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_usage_export_bucket(
        self,
    ) -> Callable[[compute.SetUsageExportBucketProjectRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetUsageExportBucket(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ProjectsRestTransport",)
