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


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.accessapproval_v1.types import accessapproval

from .base import AccessApprovalTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AccessApprovalRestInterceptor:
    """Interceptor for AccessApproval.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AccessApprovalRestTransport.

    .. code-block:: python
        class MyCustomAccessApprovalInterceptor(AccessApprovalRestInterceptor):
            def pre_approve_approval_request(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_approve_approval_request(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_access_approval_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_dismiss_approval_request(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_dismiss_approval_request(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_access_approval_service_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_access_approval_service_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_access_approval_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_access_approval_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_approval_request(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_approval_request(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_invalidate_approval_request(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_invalidate_approval_request(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_approval_requests(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_approval_requests(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_access_approval_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_access_approval_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AccessApprovalRestTransport(interceptor=MyCustomAccessApprovalInterceptor())
        client = AccessApprovalClient(transport=transport)


    """

    def pre_approve_approval_request(
        self,
        request: accessapproval.ApproveApprovalRequestMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[accessapproval.ApproveApprovalRequestMessage, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for approve_approval_request

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_approve_approval_request(
        self, response: accessapproval.ApprovalRequest
    ) -> accessapproval.ApprovalRequest:
        """Post-rpc interceptor for approve_approval_request

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response

    def pre_delete_access_approval_settings(
        self,
        request: accessapproval.DeleteAccessApprovalSettingsMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        accessapproval.DeleteAccessApprovalSettingsMessage, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_access_approval_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def pre_dismiss_approval_request(
        self,
        request: accessapproval.DismissApprovalRequestMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[accessapproval.DismissApprovalRequestMessage, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for dismiss_approval_request

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_dismiss_approval_request(
        self, response: accessapproval.ApprovalRequest
    ) -> accessapproval.ApprovalRequest:
        """Post-rpc interceptor for dismiss_approval_request

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response

    def pre_get_access_approval_service_account(
        self,
        request: accessapproval.GetAccessApprovalServiceAccountMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        accessapproval.GetAccessApprovalServiceAccountMessage, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_access_approval_service_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_get_access_approval_service_account(
        self, response: accessapproval.AccessApprovalServiceAccount
    ) -> accessapproval.AccessApprovalServiceAccount:
        """Post-rpc interceptor for get_access_approval_service_account

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response

    def pre_get_access_approval_settings(
        self,
        request: accessapproval.GetAccessApprovalSettingsMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        accessapproval.GetAccessApprovalSettingsMessage, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_access_approval_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_get_access_approval_settings(
        self, response: accessapproval.AccessApprovalSettings
    ) -> accessapproval.AccessApprovalSettings:
        """Post-rpc interceptor for get_access_approval_settings

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response

    def pre_get_approval_request(
        self,
        request: accessapproval.GetApprovalRequestMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[accessapproval.GetApprovalRequestMessage, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_approval_request

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_get_approval_request(
        self, response: accessapproval.ApprovalRequest
    ) -> accessapproval.ApprovalRequest:
        """Post-rpc interceptor for get_approval_request

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response

    def pre_invalidate_approval_request(
        self,
        request: accessapproval.InvalidateApprovalRequestMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        accessapproval.InvalidateApprovalRequestMessage, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for invalidate_approval_request

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_invalidate_approval_request(
        self, response: accessapproval.ApprovalRequest
    ) -> accessapproval.ApprovalRequest:
        """Post-rpc interceptor for invalidate_approval_request

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response

    def pre_list_approval_requests(
        self,
        request: accessapproval.ListApprovalRequestsMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[accessapproval.ListApprovalRequestsMessage, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_approval_requests

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_list_approval_requests(
        self, response: accessapproval.ListApprovalRequestsResponse
    ) -> accessapproval.ListApprovalRequestsResponse:
        """Post-rpc interceptor for list_approval_requests

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response

    def pre_update_access_approval_settings(
        self,
        request: accessapproval.UpdateAccessApprovalSettingsMessage,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        accessapproval.UpdateAccessApprovalSettingsMessage, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_access_approval_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AccessApproval server.
        """
        return request, metadata

    def post_update_access_approval_settings(
        self, response: accessapproval.AccessApprovalSettings
    ) -> accessapproval.AccessApprovalSettings:
        """Post-rpc interceptor for update_access_approval_settings

        Override in a subclass to manipulate the response
        after it is returned by the AccessApproval server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AccessApprovalRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AccessApprovalRestInterceptor


class AccessApprovalRestTransport(AccessApprovalTransport):
    """REST backend transport for AccessApproval.

    This API allows a customer to manage accesses to cloud resources by
    Google personnel. It defines the following resource model:

    -  The API has a collection of
       [ApprovalRequest][google.cloud.accessapproval.v1.ApprovalRequest]
       resources, named ``approvalRequests/{approval_request}``
    -  The API has top-level settings per Project/Folder/Organization,
       named ``accessApprovalSettings``

    The service also periodically emails a list of recipients, defined
    at the Project/Folder/Organization level in the
    accessApprovalSettings, when there is a pending ApprovalRequest for
    them to act on. The ApprovalRequests can also optionally be
    published to a Pub/Sub topic owned by the customer (contact support
    if you would like to enable Pub/Sub notifications).

    ApprovalRequests can be approved or dismissed. Google personnel can
    only access the indicated resource or resources if the request is
    approved (subject to some exclusions:
    https://cloud.google.com/access-approval/docs/overview#exclusions).

    Note: Using Access Approval functionality will mean that Google may
    not be able to meet the SLAs for your chosen products, as any
    support response times may be dramatically increased. As such the
    SLAs do not apply to any service disruption to the extent impacted
    by Customer's use of Access Approval. Do not enable Access Approval
    for projects where you may require high service availability and
    rapid response by Google Cloud Support.

    After a request is approved or dismissed, no further action may be
    taken on it. Requests with the requested_expiration in the past or
    with no activity for 14 days are considered dismissed. When an
    approval expires, the request is considered dismissed.

    If a request is not approved or dismissed, we call it pending.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "accessapproval.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AccessApprovalRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'accessapproval.googleapis.com').
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
        self._interceptor = interceptor or AccessApprovalRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _ApproveApprovalRequest(AccessApprovalRestStub):
        def __hash__(self):
            return hash("ApproveApprovalRequest")

        def __call__(
            self,
            request: accessapproval.ApproveApprovalRequestMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.ApprovalRequest:
            r"""Call the approve approval request method over HTTP.

            Args:
                request (~.accessapproval.ApproveApprovalRequestMessage):
                    The request object. Request to approve an
                ApprovalRequest.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accessapproval.ApprovalRequest:
                    A request for the customer to approve
                access to a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/approvalRequests/*}:approve",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=folders/*/approvalRequests/*}:approve",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=organizations/*/approvalRequests/*}:approve",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_approve_approval_request(
                request, metadata
            )
            pb_request = accessapproval.ApproveApprovalRequestMessage.pb(request)
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
            resp = accessapproval.ApprovalRequest()
            pb_resp = accessapproval.ApprovalRequest.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_approve_approval_request(resp)
            return resp

    class _DeleteAccessApprovalSettings(AccessApprovalRestStub):
        def __hash__(self):
            return hash("DeleteAccessApprovalSettings")

        def __call__(
            self,
            request: accessapproval.DeleteAccessApprovalSettingsMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete access approval
            settings method over HTTP.

                Args:
                    request (~.accessapproval.DeleteAccessApprovalSettingsMessage):
                        The request object. Request to delete access approval
                    settings.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/accessApprovalSettings}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=folders/*/accessApprovalSettings}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=organizations/*/accessApprovalSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_access_approval_settings(
                request, metadata
            )
            pb_request = accessapproval.DeleteAccessApprovalSettingsMessage.pb(request)
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

    class _DismissApprovalRequest(AccessApprovalRestStub):
        def __hash__(self):
            return hash("DismissApprovalRequest")

        def __call__(
            self,
            request: accessapproval.DismissApprovalRequestMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.ApprovalRequest:
            r"""Call the dismiss approval request method over HTTP.

            Args:
                request (~.accessapproval.DismissApprovalRequestMessage):
                    The request object. Request to dismiss an approval
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accessapproval.ApprovalRequest:
                    A request for the customer to approve
                access to a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/approvalRequests/*}:dismiss",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=folders/*/approvalRequests/*}:dismiss",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=organizations/*/approvalRequests/*}:dismiss",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_dismiss_approval_request(
                request, metadata
            )
            pb_request = accessapproval.DismissApprovalRequestMessage.pb(request)
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
            resp = accessapproval.ApprovalRequest()
            pb_resp = accessapproval.ApprovalRequest.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_dismiss_approval_request(resp)
            return resp

    class _GetAccessApprovalServiceAccount(AccessApprovalRestStub):
        def __hash__(self):
            return hash("GetAccessApprovalServiceAccount")

        def __call__(
            self,
            request: accessapproval.GetAccessApprovalServiceAccountMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.AccessApprovalServiceAccount:
            r"""Call the get access approval
            service account method over HTTP.

                Args:
                    request (~.accessapproval.GetAccessApprovalServiceAccountMessage):
                        The request object. Request to get an Access Approval
                    service account.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.accessapproval.AccessApprovalServiceAccount:
                        Access Approval service account
                    related to a
                    project/folder/organization.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/serviceAccount}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/serviceAccount}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/serviceAccount}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_access_approval_service_account(
                request, metadata
            )
            pb_request = accessapproval.GetAccessApprovalServiceAccountMessage.pb(
                request
            )
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
            resp = accessapproval.AccessApprovalServiceAccount()
            pb_resp = accessapproval.AccessApprovalServiceAccount.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_access_approval_service_account(resp)
            return resp

    class _GetAccessApprovalSettings(AccessApprovalRestStub):
        def __hash__(self):
            return hash("GetAccessApprovalSettings")

        def __call__(
            self,
            request: accessapproval.GetAccessApprovalSettingsMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.AccessApprovalSettings:
            r"""Call the get access approval
            settings method over HTTP.

                Args:
                    request (~.accessapproval.GetAccessApprovalSettingsMessage):
                        The request object. Request to get access approval
                    settings.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.accessapproval.AccessApprovalSettings:
                        Settings on a
                    Project/Folder/Organization related to
                    Access Approval.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/accessApprovalSettings}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/accessApprovalSettings}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/accessApprovalSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_access_approval_settings(
                request, metadata
            )
            pb_request = accessapproval.GetAccessApprovalSettingsMessage.pb(request)
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
            resp = accessapproval.AccessApprovalSettings()
            pb_resp = accessapproval.AccessApprovalSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_access_approval_settings(resp)
            return resp

    class _GetApprovalRequest(AccessApprovalRestStub):
        def __hash__(self):
            return hash("GetApprovalRequest")

        def __call__(
            self,
            request: accessapproval.GetApprovalRequestMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.ApprovalRequest:
            r"""Call the get approval request method over HTTP.

            Args:
                request (~.accessapproval.GetApprovalRequestMessage):
                    The request object. Request to get an approval request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accessapproval.ApprovalRequest:
                    A request for the customer to approve
                access to a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/approvalRequests/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/approvalRequests/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/approvalRequests/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_approval_request(
                request, metadata
            )
            pb_request = accessapproval.GetApprovalRequestMessage.pb(request)
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
            resp = accessapproval.ApprovalRequest()
            pb_resp = accessapproval.ApprovalRequest.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_approval_request(resp)
            return resp

    class _InvalidateApprovalRequest(AccessApprovalRestStub):
        def __hash__(self):
            return hash("InvalidateApprovalRequest")

        def __call__(
            self,
            request: accessapproval.InvalidateApprovalRequestMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.ApprovalRequest:
            r"""Call the invalidate approval
            request method over HTTP.

                Args:
                    request (~.accessapproval.InvalidateApprovalRequestMessage):
                        The request object. Request to invalidate an existing
                    approval.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.accessapproval.ApprovalRequest:
                        A request for the customer to approve
                    access to a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/approvalRequests/*}:invalidate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=folders/*/approvalRequests/*}:invalidate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=organizations/*/approvalRequests/*}:invalidate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_invalidate_approval_request(
                request, metadata
            )
            pb_request = accessapproval.InvalidateApprovalRequestMessage.pb(request)
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
            resp = accessapproval.ApprovalRequest()
            pb_resp = accessapproval.ApprovalRequest.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_invalidate_approval_request(resp)
            return resp

    class _ListApprovalRequests(AccessApprovalRestStub):
        def __hash__(self):
            return hash("ListApprovalRequests")

        def __call__(
            self,
            request: accessapproval.ListApprovalRequestsMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.ListApprovalRequestsResponse:
            r"""Call the list approval requests method over HTTP.

            Args:
                request (~.accessapproval.ListApprovalRequestsMessage):
                    The request object. Request to list approval requests.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.accessapproval.ListApprovalRequestsResponse:
                    Response to listing of
                ApprovalRequest objects.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/approvalRequests",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*}/approvalRequests",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*}/approvalRequests",
                },
            ]
            request, metadata = self._interceptor.pre_list_approval_requests(
                request, metadata
            )
            pb_request = accessapproval.ListApprovalRequestsMessage.pb(request)
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
            resp = accessapproval.ListApprovalRequestsResponse()
            pb_resp = accessapproval.ListApprovalRequestsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_approval_requests(resp)
            return resp

    class _UpdateAccessApprovalSettings(AccessApprovalRestStub):
        def __hash__(self):
            return hash("UpdateAccessApprovalSettings")

        def __call__(
            self,
            request: accessapproval.UpdateAccessApprovalSettingsMessage,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> accessapproval.AccessApprovalSettings:
            r"""Call the update access approval
            settings method over HTTP.

                Args:
                    request (~.accessapproval.UpdateAccessApprovalSettingsMessage):
                        The request object. Request to update access approval
                    settings.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.accessapproval.AccessApprovalSettings:
                        Settings on a
                    Project/Folder/Organization related to
                    Access Approval.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{settings.name=projects/*/accessApprovalSettings}",
                    "body": "settings",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{settings.name=folders/*/accessApprovalSettings}",
                    "body": "settings",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{settings.name=organizations/*/accessApprovalSettings}",
                    "body": "settings",
                },
            ]
            request, metadata = self._interceptor.pre_update_access_approval_settings(
                request, metadata
            )
            pb_request = accessapproval.UpdateAccessApprovalSettingsMessage.pb(request)
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
            resp = accessapproval.AccessApprovalSettings()
            pb_resp = accessapproval.AccessApprovalSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_access_approval_settings(resp)
            return resp

    @property
    def approve_approval_request(
        self,
    ) -> Callable[
        [accessapproval.ApproveApprovalRequestMessage], accessapproval.ApprovalRequest
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApproveApprovalRequest(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_access_approval_settings(
        self,
    ) -> Callable[
        [accessapproval.DeleteAccessApprovalSettingsMessage], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAccessApprovalSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def dismiss_approval_request(
        self,
    ) -> Callable[
        [accessapproval.DismissApprovalRequestMessage], accessapproval.ApprovalRequest
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DismissApprovalRequest(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_access_approval_service_account(
        self,
    ) -> Callable[
        [accessapproval.GetAccessApprovalServiceAccountMessage],
        accessapproval.AccessApprovalServiceAccount,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccessApprovalServiceAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_access_approval_settings(
        self,
    ) -> Callable[
        [accessapproval.GetAccessApprovalSettingsMessage],
        accessapproval.AccessApprovalSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccessApprovalSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_approval_request(
        self,
    ) -> Callable[
        [accessapproval.GetApprovalRequestMessage], accessapproval.ApprovalRequest
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApprovalRequest(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def invalidate_approval_request(
        self,
    ) -> Callable[
        [accessapproval.InvalidateApprovalRequestMessage],
        accessapproval.ApprovalRequest,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InvalidateApprovalRequest(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_approval_requests(
        self,
    ) -> Callable[
        [accessapproval.ListApprovalRequestsMessage],
        accessapproval.ListApprovalRequestsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApprovalRequests(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_access_approval_settings(
        self,
    ) -> Callable[
        [accessapproval.UpdateAccessApprovalSettingsMessage],
        accessapproval.AccessApprovalSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAccessApprovalSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AccessApprovalRestTransport",)
