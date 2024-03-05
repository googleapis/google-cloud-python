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

from google.cloud.gsuiteaddons_v1.types import gsuiteaddons

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import GSuiteAddOnsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class GSuiteAddOnsRestInterceptor:
    """Interceptor for GSuiteAddOns.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the GSuiteAddOnsRestTransport.

    .. code-block:: python
        class MyCustomGSuiteAddOnsInterceptor(GSuiteAddOnsRestInterceptor):
            def pre_create_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_authorization(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_authorization(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_install_status(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_install_status(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_install_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_list_deployments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_deployments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_replace_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_replace_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_uninstall_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

        transport = GSuiteAddOnsRestTransport(interceptor=MyCustomGSuiteAddOnsInterceptor())
        client = GSuiteAddOnsClient(transport=transport)


    """

    def pre_create_deployment(
        self,
        request: gsuiteaddons.CreateDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.CreateDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def post_create_deployment(
        self, response: gsuiteaddons.Deployment
    ) -> gsuiteaddons.Deployment:
        """Post-rpc interceptor for create_deployment

        Override in a subclass to manipulate the response
        after it is returned by the GSuiteAddOns server but before
        it is returned to user code.
        """
        return response

    def pre_delete_deployment(
        self,
        request: gsuiteaddons.DeleteDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.DeleteDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def pre_get_authorization(
        self,
        request: gsuiteaddons.GetAuthorizationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.GetAuthorizationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_authorization

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def post_get_authorization(
        self, response: gsuiteaddons.Authorization
    ) -> gsuiteaddons.Authorization:
        """Post-rpc interceptor for get_authorization

        Override in a subclass to manipulate the response
        after it is returned by the GSuiteAddOns server but before
        it is returned to user code.
        """
        return response

    def pre_get_deployment(
        self,
        request: gsuiteaddons.GetDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.GetDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def post_get_deployment(
        self, response: gsuiteaddons.Deployment
    ) -> gsuiteaddons.Deployment:
        """Post-rpc interceptor for get_deployment

        Override in a subclass to manipulate the response
        after it is returned by the GSuiteAddOns server but before
        it is returned to user code.
        """
        return response

    def pre_get_install_status(
        self,
        request: gsuiteaddons.GetInstallStatusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.GetInstallStatusRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_install_status

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def post_get_install_status(
        self, response: gsuiteaddons.InstallStatus
    ) -> gsuiteaddons.InstallStatus:
        """Post-rpc interceptor for get_install_status

        Override in a subclass to manipulate the response
        after it is returned by the GSuiteAddOns server but before
        it is returned to user code.
        """
        return response

    def pre_install_deployment(
        self,
        request: gsuiteaddons.InstallDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.InstallDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for install_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def pre_list_deployments(
        self,
        request: gsuiteaddons.ListDeploymentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.ListDeploymentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_deployments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def post_list_deployments(
        self, response: gsuiteaddons.ListDeploymentsResponse
    ) -> gsuiteaddons.ListDeploymentsResponse:
        """Post-rpc interceptor for list_deployments

        Override in a subclass to manipulate the response
        after it is returned by the GSuiteAddOns server but before
        it is returned to user code.
        """
        return response

    def pre_replace_deployment(
        self,
        request: gsuiteaddons.ReplaceDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.ReplaceDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for replace_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata

    def post_replace_deployment(
        self, response: gsuiteaddons.Deployment
    ) -> gsuiteaddons.Deployment:
        """Post-rpc interceptor for replace_deployment

        Override in a subclass to manipulate the response
        after it is returned by the GSuiteAddOns server but before
        it is returned to user code.
        """
        return response

    def pre_uninstall_deployment(
        self,
        request: gsuiteaddons.UninstallDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsuiteaddons.UninstallDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for uninstall_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GSuiteAddOns server.
        """
        return request, metadata


@dataclasses.dataclass
class GSuiteAddOnsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: GSuiteAddOnsRestInterceptor


class GSuiteAddOnsRestTransport(GSuiteAddOnsTransport):
    """REST backend transport for GSuiteAddOns.

    A service for managing Google Workspace Add-ons deployments.

    A Google Workspace Add-on is a third-party embedded component
    that can be installed in Google Workspace Applications like
    Gmail, Calendar, Drive, and the Google Docs, Sheets, and Slides
    editors. Google Workspace Add-ons can display UI cards, receive
    contextual information from the host application, and perform
    actions in the host application (See:

    https://developers.google.com/gsuite/add-ons/overview for more
    information).

    A Google Workspace Add-on deployment resource specifies metadata
    about the add-on, including a specification of the entry points
    in the host application that trigger add-on executions (see:

    https://developers.google.com/gsuite/add-ons/concepts/gsuite-manifests).
    Add-on deployments defined via the Google Workspace Add-ons API
    define their entrypoints using HTTPS URLs (See:

    https://developers.google.com/gsuite/add-ons/guides/alternate-runtimes),

    A Google Workspace Add-on deployment can be installed in
    developer mode, which allows an add-on developer to test the
    experience an end-user would see when installing and running the
    add-on in their G Suite applications.  When running in developer
    mode, more detailed error messages are exposed in the add-on UI
    to aid in debugging.

    A Google Workspace Add-on deployment can be published to Google
    Workspace Marketplace, which allows other Google Workspace users
    to discover and install the add-on.  See:

    https://developers.google.com/gsuite/add-ons/how-tos/publish-add-on-overview
    for details.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "gsuiteaddons.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[GSuiteAddOnsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'gsuiteaddons.googleapis.com').
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
        self._interceptor = interceptor or GSuiteAddOnsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDeployment(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("CreateDeployment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "deploymentId": "",
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
            request: gsuiteaddons.CreateDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsuiteaddons.Deployment:
            r"""Call the create deployment method over HTTP.

            Args:
                request (~.gsuiteaddons.CreateDeploymentRequest):
                    The request object. Request message to create a
                deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsuiteaddons.Deployment:
                    A Google Workspace Add-on deployment
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/deployments",
                    "body": "deployment",
                },
            ]
            request, metadata = self._interceptor.pre_create_deployment(
                request, metadata
            )
            pb_request = gsuiteaddons.CreateDeploymentRequest.pb(request)
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
            resp = gsuiteaddons.Deployment()
            pb_resp = gsuiteaddons.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_deployment(resp)
            return resp

    class _DeleteDeployment(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("DeleteDeployment")

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
            request: gsuiteaddons.DeleteDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete deployment method over HTTP.

            Args:
                request (~.gsuiteaddons.DeleteDeploymentRequest):
                    The request object. Request message to delete a
                deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/deployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_deployment(
                request, metadata
            )
            pb_request = gsuiteaddons.DeleteDeploymentRequest.pb(request)
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

    class _GetAuthorization(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("GetAuthorization")

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
            request: gsuiteaddons.GetAuthorizationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsuiteaddons.Authorization:
            r"""Call the get authorization method over HTTP.

            Args:
                request (~.gsuiteaddons.GetAuthorizationRequest):
                    The request object. Request message to get Google
                Workspace Add-ons authorization
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsuiteaddons.Authorization:
                    The authorization information used
                when invoking deployment endpoints.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/authorization}",
                },
            ]
            request, metadata = self._interceptor.pre_get_authorization(
                request, metadata
            )
            pb_request = gsuiteaddons.GetAuthorizationRequest.pb(request)
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
            resp = gsuiteaddons.Authorization()
            pb_resp = gsuiteaddons.Authorization.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_authorization(resp)
            return resp

    class _GetDeployment(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("GetDeployment")

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
            request: gsuiteaddons.GetDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsuiteaddons.Deployment:
            r"""Call the get deployment method over HTTP.

            Args:
                request (~.gsuiteaddons.GetDeploymentRequest):
                    The request object. Request message to get a deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsuiteaddons.Deployment:
                    A Google Workspace Add-on deployment
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/deployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_deployment(request, metadata)
            pb_request = gsuiteaddons.GetDeploymentRequest.pb(request)
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
            resp = gsuiteaddons.Deployment()
            pb_resp = gsuiteaddons.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_deployment(resp)
            return resp

    class _GetInstallStatus(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("GetInstallStatus")

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
            request: gsuiteaddons.GetInstallStatusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsuiteaddons.InstallStatus:
            r"""Call the get install status method over HTTP.

            Args:
                request (~.gsuiteaddons.GetInstallStatusRequest):
                    The request object. Request message to get the install
                status of a developer mode deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsuiteaddons.InstallStatus:
                    Developer mode install status of a
                deployment

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/deployments/*/installStatus}",
                },
            ]
            request, metadata = self._interceptor.pre_get_install_status(
                request, metadata
            )
            pb_request = gsuiteaddons.GetInstallStatusRequest.pb(request)
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
            resp = gsuiteaddons.InstallStatus()
            pb_resp = gsuiteaddons.InstallStatus.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_install_status(resp)
            return resp

    class _InstallDeployment(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("InstallDeployment")

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
            request: gsuiteaddons.InstallDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the install deployment method over HTTP.

            Args:
                request (~.gsuiteaddons.InstallDeploymentRequest):
                    The request object. Request message to install a
                developer mode deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/deployments/*}:install",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_install_deployment(
                request, metadata
            )
            pb_request = gsuiteaddons.InstallDeploymentRequest.pb(request)
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

    class _ListDeployments(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("ListDeployments")

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
            request: gsuiteaddons.ListDeploymentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsuiteaddons.ListDeploymentsResponse:
            r"""Call the list deployments method over HTTP.

            Args:
                request (~.gsuiteaddons.ListDeploymentsRequest):
                    The request object. Request message to list deployments
                for a project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsuiteaddons.ListDeploymentsResponse:
                    Response message to list deployments.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/deployments",
                },
            ]
            request, metadata = self._interceptor.pre_list_deployments(
                request, metadata
            )
            pb_request = gsuiteaddons.ListDeploymentsRequest.pb(request)
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
            resp = gsuiteaddons.ListDeploymentsResponse()
            pb_resp = gsuiteaddons.ListDeploymentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_deployments(resp)
            return resp

    class _ReplaceDeployment(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("ReplaceDeployment")

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
            request: gsuiteaddons.ReplaceDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsuiteaddons.Deployment:
            r"""Call the replace deployment method over HTTP.

            Args:
                request (~.gsuiteaddons.ReplaceDeploymentRequest):
                    The request object. Request message to create or replace
                a deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsuiteaddons.Deployment:
                    A Google Workspace Add-on deployment
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1/{deployment.name=projects/*/deployments/*}",
                    "body": "deployment",
                },
            ]
            request, metadata = self._interceptor.pre_replace_deployment(
                request, metadata
            )
            pb_request = gsuiteaddons.ReplaceDeploymentRequest.pb(request)
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
            resp = gsuiteaddons.Deployment()
            pb_resp = gsuiteaddons.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_replace_deployment(resp)
            return resp

    class _UninstallDeployment(GSuiteAddOnsRestStub):
        def __hash__(self):
            return hash("UninstallDeployment")

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
            request: gsuiteaddons.UninstallDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the uninstall deployment method over HTTP.

            Args:
                request (~.gsuiteaddons.UninstallDeploymentRequest):
                    The request object. Request message to uninstall a
                developer mode deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/deployments/*}:uninstall",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_uninstall_deployment(
                request, metadata
            )
            pb_request = gsuiteaddons.UninstallDeploymentRequest.pb(request)
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

    @property
    def create_deployment(
        self,
    ) -> Callable[[gsuiteaddons.CreateDeploymentRequest], gsuiteaddons.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_deployment(
        self,
    ) -> Callable[[gsuiteaddons.DeleteDeploymentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_authorization(
        self,
    ) -> Callable[[gsuiteaddons.GetAuthorizationRequest], gsuiteaddons.Authorization]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAuthorization(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_deployment(
        self,
    ) -> Callable[[gsuiteaddons.GetDeploymentRequest], gsuiteaddons.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_install_status(
        self,
    ) -> Callable[[gsuiteaddons.GetInstallStatusRequest], gsuiteaddons.InstallStatus]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInstallStatus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def install_deployment(
        self,
    ) -> Callable[[gsuiteaddons.InstallDeploymentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InstallDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_deployments(
        self,
    ) -> Callable[
        [gsuiteaddons.ListDeploymentsRequest], gsuiteaddons.ListDeploymentsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeployments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def replace_deployment(
        self,
    ) -> Callable[[gsuiteaddons.ReplaceDeploymentRequest], gsuiteaddons.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReplaceDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def uninstall_deployment(
        self,
    ) -> Callable[[gsuiteaddons.UninstallDeploymentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UninstallDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("GSuiteAddOnsRestTransport",)
