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
import logging
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
from .rest_base import _BaseRegionDisksRestTransport

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


class RegionDisksRestInterceptor:
    """Interceptor for RegionDisks.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionDisksRestTransport.

    .. code-block:: python
        class MyCustomRegionDisksInterceptor(RegionDisksRestInterceptor):
            def pre_add_resource_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_resource_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_bulk_insert(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_bulk_insert(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
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

            def pre_remove_resource_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_resource_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resize(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resize(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_labels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_labels(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_async_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_async_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_async_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_async_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_group_async_replication(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_group_async_replication(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RegionDisksRestTransport(interceptor=MyCustomRegionDisksInterceptor())
        client = RegionDisksClient(transport=transport)


    """

    def pre_add_resource_policies(
        self,
        request: compute.AddResourcePoliciesRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.AddResourcePoliciesRegionDiskRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for add_resource_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_add_resource_policies(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for add_resource_policies

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_bulk_insert(
        self,
        request: compute.BulkInsertRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.BulkInsertRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for bulk_insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_bulk_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for bulk_insert

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_create_snapshot(
        self,
        request: compute.CreateSnapshotRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.CreateSnapshotRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_create_snapshot(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for create_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeleteRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.DeleteRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.GetRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_get(self, response: compute.Disk) -> compute.Disk:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: compute.GetIamPolicyRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.GetIamPolicyRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: compute.Policy) -> compute.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.InsertRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListRegionDisksRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.ListRegionDisksRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_list(self, response: compute.DiskList) -> compute.DiskList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_remove_resource_policies(
        self,
        request: compute.RemoveResourcePoliciesRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.RemoveResourcePoliciesRegionDiskRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for remove_resource_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_remove_resource_policies(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for remove_resource_policies

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_resize(
        self,
        request: compute.ResizeRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.ResizeRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for resize

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_resize(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for resize

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: compute.SetIamPolicyRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.SetIamPolicyRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: compute.Policy) -> compute.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_set_labels(
        self,
        request: compute.SetLabelsRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.SetLabelsRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for set_labels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_set_labels(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_labels

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_start_async_replication(
        self,
        request: compute.StartAsyncReplicationRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.StartAsyncReplicationRegionDiskRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for start_async_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_start_async_replication(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for start_async_replication

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_stop_async_replication(
        self,
        request: compute.StopAsyncReplicationRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.StopAsyncReplicationRegionDiskRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for stop_async_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_stop_async_replication(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for stop_async_replication

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_stop_group_async_replication(
        self,
        request: compute.StopGroupAsyncReplicationRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.StopGroupAsyncReplicationRegionDiskRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for stop_group_async_replication

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_stop_group_async_replication(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for stop_group_async_replication

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: compute.TestIamPermissionsRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.TestIamPermissionsRegionDiskRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: compute.TestPermissionsResponse
    ) -> compute.TestPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response

    def pre_update(
        self,
        request: compute.UpdateRegionDiskRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.UpdateRegionDiskRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionDisks server.
        """
        return request, metadata

    def post_update(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for update

        Override in a subclass to manipulate the response
        after it is returned by the RegionDisks server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionDisksRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionDisksRestInterceptor


class RegionDisksRestTransport(_BaseRegionDisksRestTransport):
    """REST backend synchronous transport for RegionDisks.

    The RegionDisks API.

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
        interceptor: Optional[RegionDisksRestInterceptor] = None,
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
        self._interceptor = interceptor or RegionDisksRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AddResourcePolicies(
        _BaseRegionDisksRestTransport._BaseAddResourcePolicies, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.AddResourcePolicies")

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
            request: compute.AddResourcePoliciesRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the add resource policies method over HTTP.

            Args:
                request (~.compute.AddResourcePoliciesRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.AddResourcePolicies. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseAddResourcePolicies._get_http_options()
            )

            request, metadata = self._interceptor.pre_add_resource_policies(
                request, metadata
            )
            transcoded_request = _BaseRegionDisksRestTransport._BaseAddResourcePolicies._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionDisksRestTransport._BaseAddResourcePolicies._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionDisksRestTransport._BaseAddResourcePolicies._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.AddResourcePolicies",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "AddResourcePolicies",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._AddResourcePolicies._get_response(
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

            resp = self._interceptor.post_add_resource_policies(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.add_resource_policies",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "AddResourcePolicies",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _BulkInsert(
        _BaseRegionDisksRestTransport._BaseBulkInsert, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.BulkInsert")

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
            request: compute.BulkInsertRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the bulk insert method over HTTP.

            Args:
                request (~.compute.BulkInsertRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.BulkInsert. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseBulkInsert._get_http_options()
            )

            request, metadata = self._interceptor.pre_bulk_insert(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseBulkInsert._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionDisksRestTransport._BaseBulkInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseBulkInsert._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.BulkInsert",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "BulkInsert",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._BulkInsert._get_response(
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

            resp = self._interceptor.post_bulk_insert(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.bulk_insert",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "BulkInsert",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateSnapshot(
        _BaseRegionDisksRestTransport._BaseCreateSnapshot, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.CreateSnapshot")

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
            request: compute.CreateSnapshotRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the create snapshot method over HTTP.

            Args:
                request (~.compute.CreateSnapshotRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.CreateSnapshot. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseCreateSnapshot._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_snapshot(request, metadata)
            transcoded_request = _BaseRegionDisksRestTransport._BaseCreateSnapshot._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionDisksRestTransport._BaseCreateSnapshot._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionDisksRestTransport._BaseCreateSnapshot._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.CreateSnapshot",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "CreateSnapshot",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._CreateSnapshot._get_response(
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

            resp = self._interceptor.post_create_snapshot(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.create_snapshot",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "CreateSnapshot",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Delete(_BaseRegionDisksRestTransport._BaseDelete, RegionDisksRestStub):
        def __hash__(self):
            return hash("RegionDisksRestTransport.Delete")

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
            request: compute.DeleteRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.Delete. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = _BaseRegionDisksRestTransport._BaseDelete._get_http_options()

            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseDelete._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseDelete._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.Delete",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Delete",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._Delete._get_response(
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.delete",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Delete",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Get(_BaseRegionDisksRestTransport._BaseGet, RegionDisksRestStub):
        def __hash__(self):
            return hash("RegionDisksRestTransport.Get")

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
            request: compute.GetRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Disk:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.Get. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Disk:
                    Represents a Persistent Disk resource. Google Compute
                Engine has two Disk resources: \*
                `Zonal </compute/docs/reference/rest/v1/disks>`__ \*
                `Regional </compute/docs/reference/rest/v1/regionDisks>`__
                Persistent disks are required for running your VM
                instances. Create both boot and non-boot (data)
                persistent disks. For more information, read Persistent
                Disks. For more storage options, read Storage options.
                The disks resource represents a zonal persistent disk.
                For more information, read Zonal persistent disks. The
                regionDisks resource represents a regional persistent
                disk. For more information, read Regional resources.

            """

            http_options = _BaseRegionDisksRestTransport._BaseGet._get_http_options()

            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseGet._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseGet._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.Get",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Get",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._Get._get_response(
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
            resp = compute.Disk()
            pb_resp = compute.Disk.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Disk.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.get",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Get",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetIamPolicy(
        _BaseRegionDisksRestTransport._BaseGetIamPolicy, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.GetIamPolicy")

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
            request: compute.GetIamPolicyRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.compute.GetIamPolicyRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.GetIamPolicy. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role. For some types of Google
                Cloud resources, a ``binding`` can also specify a
                ``condition``, which is a logical expression that allows
                access to a resource only if the expression evaluates to
                ``true``. A condition can add constraints based on
                attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:**
                ``{ "bindings": [ { "role": "roles/resourcemanager.organizationAdmin", "members": [ "user:mike@example.com", "group:admins@example.com", "domain:google.com", "serviceAccount:my-project-id@appspot.gserviceaccount.com" ] }, { "role": "roles/resourcemanager.organizationViewer", "members": [ "user:eve@example.com" ], "condition": { "title": "expirable access", "description": "Does not grant access after Sep 2020", "expression": "request.time < timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag": "BwWWja0YfJA=", "version": 3 }``
                **YAML example:**
                ``bindings: - members: - user:mike@example.com - group:admins@example.com - domain:google.com - serviceAccount:my-project-id@appspot.gserviceaccount.com role: roles/resourcemanager.organizationAdmin - members: - user:eve@example.com role: roles/resourcemanager.organizationViewer condition: title: expirable access description: Does not grant access after Sep 2020 expression: request.time < timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA= version: 3``
                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseRegionDisksRestTransport._BaseGetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseGetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseGetIamPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "GetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._GetIamPolicy._get_response(
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
            resp = compute.Policy()
            pb_resp = compute.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Policy.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.get_iam_policy",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "GetIamPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Insert(_BaseRegionDisksRestTransport._BaseInsert, RegionDisksRestStub):
        def __hash__(self):
            return hash("RegionDisksRestTransport.Insert")

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
            request: compute.InsertRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.Insert. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = _BaseRegionDisksRestTransport._BaseInsert._get_http_options()

            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseInsert._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionDisksRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseInsert._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.Insert",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Insert",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._Insert._get_response(
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.insert",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Insert",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _List(_BaseRegionDisksRestTransport._BaseList, RegionDisksRestStub):
        def __hash__(self):
            return hash("RegionDisksRestTransport.List")

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
            request: compute.ListRegionDisksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.DiskList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionDisksRequest):
                    The request object. A request message for
                RegionDisks.List. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.DiskList:
                    A list of Disk resources.
            """

            http_options = _BaseRegionDisksRestTransport._BaseList._get_http_options()

            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseList._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseList._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.List",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "List",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._List._get_response(
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
            resp = compute.DiskList()
            pb_resp = compute.DiskList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.DiskList.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.list",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "List",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RemoveResourcePolicies(
        _BaseRegionDisksRestTransport._BaseRemoveResourcePolicies, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.RemoveResourcePolicies")

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
            request: compute.RemoveResourcePoliciesRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the remove resource policies method over HTTP.

            Args:
                request (~.compute.RemoveResourcePoliciesRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.RemoveResourcePolicies. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseRemoveResourcePolicies._get_http_options()
            )

            request, metadata = self._interceptor.pre_remove_resource_policies(
                request, metadata
            )
            transcoded_request = _BaseRegionDisksRestTransport._BaseRemoveResourcePolicies._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionDisksRestTransport._BaseRemoveResourcePolicies._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionDisksRestTransport._BaseRemoveResourcePolicies._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.RemoveResourcePolicies",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "RemoveResourcePolicies",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._RemoveResourcePolicies._get_response(
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

            resp = self._interceptor.post_remove_resource_policies(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.remove_resource_policies",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "RemoveResourcePolicies",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Resize(_BaseRegionDisksRestTransport._BaseResize, RegionDisksRestStub):
        def __hash__(self):
            return hash("RegionDisksRestTransport.Resize")

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
            request: compute.ResizeRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the resize method over HTTP.

            Args:
                request (~.compute.ResizeRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.Resize. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = _BaseRegionDisksRestTransport._BaseResize._get_http_options()

            request, metadata = self._interceptor.pre_resize(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseResize._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionDisksRestTransport._BaseResize._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseResize._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.Resize",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Resize",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._Resize._get_response(
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

            resp = self._interceptor.post_resize(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.resize",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Resize",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SetIamPolicy(
        _BaseRegionDisksRestTransport._BaseSetIamPolicy, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.SetIamPolicy")

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
            request: compute.SetIamPolicyRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.compute.SetIamPolicyRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.SetIamPolicy. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role. For some types of Google
                Cloud resources, a ``binding`` can also specify a
                ``condition``, which is a logical expression that allows
                access to a resource only if the expression evaluates to
                ``true``. A condition can add constraints based on
                attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:**
                ``{ "bindings": [ { "role": "roles/resourcemanager.organizationAdmin", "members": [ "user:mike@example.com", "group:admins@example.com", "domain:google.com", "serviceAccount:my-project-id@appspot.gserviceaccount.com" ] }, { "role": "roles/resourcemanager.organizationViewer", "members": [ "user:eve@example.com" ], "condition": { "title": "expirable access", "description": "Does not grant access after Sep 2020", "expression": "request.time < timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag": "BwWWja0YfJA=", "version": 3 }``
                **YAML example:**
                ``bindings: - members: - user:mike@example.com - group:admins@example.com - domain:google.com - serviceAccount:my-project-id@appspot.gserviceaccount.com role: roles/resourcemanager.organizationAdmin - members: - user:eve@example.com role: roles/resourcemanager.organizationViewer condition: title: expirable access description: Does not grant access after Sep 2020 expression: request.time < timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA= version: 3``
                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseRegionDisksRestTransport._BaseSetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseSetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseRegionDisksRestTransport._BaseSetIamPolicy._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseSetIamPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "SetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._SetIamPolicy._get_response(
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
            resp = compute.Policy()
            pb_resp = compute.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_set_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Policy.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.set_iam_policy",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "SetIamPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SetLabels(_BaseRegionDisksRestTransport._BaseSetLabels, RegionDisksRestStub):
        def __hash__(self):
            return hash("RegionDisksRestTransport.SetLabels")

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
            request: compute.SetLabelsRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the set labels method over HTTP.

            Args:
                request (~.compute.SetLabelsRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.SetLabels. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseSetLabels._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_labels(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseSetLabels._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionDisksRestTransport._BaseSetLabels._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseSetLabels._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.SetLabels",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "SetLabels",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._SetLabels._get_response(
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

            resp = self._interceptor.post_set_labels(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.set_labels",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "SetLabels",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _StartAsyncReplication(
        _BaseRegionDisksRestTransport._BaseStartAsyncReplication, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.StartAsyncReplication")

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
            request: compute.StartAsyncReplicationRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the start async replication method over HTTP.

            Args:
                request (~.compute.StartAsyncReplicationRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.StartAsyncReplication. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseStartAsyncReplication._get_http_options()
            )

            request, metadata = self._interceptor.pre_start_async_replication(
                request, metadata
            )
            transcoded_request = _BaseRegionDisksRestTransport._BaseStartAsyncReplication._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionDisksRestTransport._BaseStartAsyncReplication._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionDisksRestTransport._BaseStartAsyncReplication._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.StartAsyncReplication",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "StartAsyncReplication",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._StartAsyncReplication._get_response(
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

            resp = self._interceptor.post_start_async_replication(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.start_async_replication",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "StartAsyncReplication",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _StopAsyncReplication(
        _BaseRegionDisksRestTransport._BaseStopAsyncReplication, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.StopAsyncReplication")

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
            request: compute.StopAsyncReplicationRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the stop async replication method over HTTP.

            Args:
                request (~.compute.StopAsyncReplicationRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.StopAsyncReplication. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseStopAsyncReplication._get_http_options()
            )

            request, metadata = self._interceptor.pre_stop_async_replication(
                request, metadata
            )
            transcoded_request = _BaseRegionDisksRestTransport._BaseStopAsyncReplication._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegionDisksRestTransport._BaseStopAsyncReplication._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.StopAsyncReplication",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "StopAsyncReplication",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._StopAsyncReplication._get_response(
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

            resp = self._interceptor.post_stop_async_replication(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.stop_async_replication",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "StopAsyncReplication",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _StopGroupAsyncReplication(
        _BaseRegionDisksRestTransport._BaseStopGroupAsyncReplication,
        RegionDisksRestStub,
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.StopGroupAsyncReplication")

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
            request: compute.StopGroupAsyncReplicationRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the stop group async
            replication method over HTTP.

                Args:
                    request (~.compute.StopGroupAsyncReplicationRegionDiskRequest):
                        The request object. A request message for
                    RegionDisks.StopGroupAsyncReplication.
                    See the method description for details.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

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
                _BaseRegionDisksRestTransport._BaseStopGroupAsyncReplication._get_http_options()
            )

            request, metadata = self._interceptor.pre_stop_group_async_replication(
                request, metadata
            )
            transcoded_request = _BaseRegionDisksRestTransport._BaseStopGroupAsyncReplication._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionDisksRestTransport._BaseStopGroupAsyncReplication._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionDisksRestTransport._BaseStopGroupAsyncReplication._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.StopGroupAsyncReplication",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "StopGroupAsyncReplication",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                RegionDisksRestTransport._StopGroupAsyncReplication._get_response(
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

            resp = self._interceptor.post_stop_group_async_replication(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.stop_group_async_replication",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "StopGroupAsyncReplication",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _TestIamPermissions(
        _BaseRegionDisksRestTransport._BaseTestIamPermissions, RegionDisksRestStub
    ):
        def __hash__(self):
            return hash("RegionDisksRestTransport.TestIamPermissions")

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
            request: compute.TestIamPermissionsRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.TestPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.compute.TestIamPermissionsRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.TestIamPermissions. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.TestPermissionsResponse:

            """

            http_options = (
                _BaseRegionDisksRestTransport._BaseTestIamPermissions._get_http_options()
            )

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseRegionDisksRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegionDisksRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegionDisksRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._TestIamPermissions._get_response(
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
            resp = compute.TestPermissionsResponse()
            pb_resp = compute.TestPermissionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_test_iam_permissions(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.TestPermissionsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.test_iam_permissions",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "TestIamPermissions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Update(_BaseRegionDisksRestTransport._BaseUpdate, RegionDisksRestStub):
        def __hash__(self):
            return hash("RegionDisksRestTransport.Update")

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
            request: compute.UpdateRegionDiskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the update method over HTTP.

            Args:
                request (~.compute.UpdateRegionDiskRequest):
                    The request object. A request message for
                RegionDisks.Update. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = _BaseRegionDisksRestTransport._BaseUpdate._get_http_options()

            request, metadata = self._interceptor.pre_update(request, metadata)
            transcoded_request = (
                _BaseRegionDisksRestTransport._BaseUpdate._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionDisksRestTransport._BaseUpdate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionDisksRestTransport._BaseUpdate._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1.RegionDisksClient.Update",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Update",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegionDisksRestTransport._Update._get_response(
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

            resp = self._interceptor.post_update(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1.RegionDisksClient.update",
                    extra={
                        "serviceName": "google.cloud.compute.v1.RegionDisks",
                        "rpcName": "Update",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def add_resource_policies(
        self,
    ) -> Callable[[compute.AddResourcePoliciesRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddResourcePolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def bulk_insert(
        self,
    ) -> Callable[[compute.BulkInsertRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BulkInsert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_snapshot(
        self,
    ) -> Callable[[compute.CreateSnapshotRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(self) -> Callable[[compute.DeleteRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(self) -> Callable[[compute.GetRegionDiskRequest], compute.Disk]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[compute.GetIamPolicyRegionDiskRequest], compute.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(self) -> Callable[[compute.InsertRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(self) -> Callable[[compute.ListRegionDisksRequest], compute.DiskList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_resource_policies(
        self,
    ) -> Callable[[compute.RemoveResourcePoliciesRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveResourcePolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resize(self) -> Callable[[compute.ResizeRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Resize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[compute.SetIamPolicyRegionDiskRequest], compute.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_labels(
        self,
    ) -> Callable[[compute.SetLabelsRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetLabels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_async_replication(
        self,
    ) -> Callable[[compute.StartAsyncReplicationRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartAsyncReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_async_replication(
        self,
    ) -> Callable[[compute.StopAsyncReplicationRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopAsyncReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_group_async_replication(
        self,
    ) -> Callable[
        [compute.StopGroupAsyncReplicationRegionDiskRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopGroupAsyncReplication(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsRegionDiskRequest], compute.TestPermissionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update(self) -> Callable[[compute.UpdateRegionDiskRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Update(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegionDisksRestTransport",)
