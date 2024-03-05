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

from google.cloud.appengine_admin_v1.types import appengine, firewall

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import FirewallTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class FirewallRestInterceptor:
    """Interceptor for Firewall.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the FirewallRestTransport.

    .. code-block:: python
        class MyCustomFirewallInterceptor(FirewallRestInterceptor):
            def pre_batch_update_ingress_rules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_ingress_rules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_ingress_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_ingress_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_ingress_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_ingress_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_ingress_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_ingress_rules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_ingress_rules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_ingress_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_ingress_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = FirewallRestTransport(interceptor=MyCustomFirewallInterceptor())
        client = FirewallClient(transport=transport)


    """

    def pre_batch_update_ingress_rules(
        self,
        request: appengine.BatchUpdateIngressRulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.BatchUpdateIngressRulesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_update_ingress_rules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firewall server.
        """
        return request, metadata

    def post_batch_update_ingress_rules(
        self, response: appengine.BatchUpdateIngressRulesResponse
    ) -> appengine.BatchUpdateIngressRulesResponse:
        """Post-rpc interceptor for batch_update_ingress_rules

        Override in a subclass to manipulate the response
        after it is returned by the Firewall server but before
        it is returned to user code.
        """
        return response

    def pre_create_ingress_rule(
        self,
        request: appengine.CreateIngressRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.CreateIngressRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_ingress_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firewall server.
        """
        return request, metadata

    def post_create_ingress_rule(
        self, response: firewall.FirewallRule
    ) -> firewall.FirewallRule:
        """Post-rpc interceptor for create_ingress_rule

        Override in a subclass to manipulate the response
        after it is returned by the Firewall server but before
        it is returned to user code.
        """
        return response

    def pre_delete_ingress_rule(
        self,
        request: appengine.DeleteIngressRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.DeleteIngressRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_ingress_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firewall server.
        """
        return request, metadata

    def pre_get_ingress_rule(
        self,
        request: appengine.GetIngressRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.GetIngressRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_ingress_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firewall server.
        """
        return request, metadata

    def post_get_ingress_rule(
        self, response: firewall.FirewallRule
    ) -> firewall.FirewallRule:
        """Post-rpc interceptor for get_ingress_rule

        Override in a subclass to manipulate the response
        after it is returned by the Firewall server but before
        it is returned to user code.
        """
        return response

    def pre_list_ingress_rules(
        self,
        request: appengine.ListIngressRulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.ListIngressRulesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_ingress_rules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firewall server.
        """
        return request, metadata

    def post_list_ingress_rules(
        self, response: appengine.ListIngressRulesResponse
    ) -> appengine.ListIngressRulesResponse:
        """Post-rpc interceptor for list_ingress_rules

        Override in a subclass to manipulate the response
        after it is returned by the Firewall server but before
        it is returned to user code.
        """
        return response

    def pre_update_ingress_rule(
        self,
        request: appengine.UpdateIngressRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.UpdateIngressRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_ingress_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firewall server.
        """
        return request, metadata

    def post_update_ingress_rule(
        self, response: firewall.FirewallRule
    ) -> firewall.FirewallRule:
        """Post-rpc interceptor for update_ingress_rule

        Override in a subclass to manipulate the response
        after it is returned by the Firewall server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class FirewallRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: FirewallRestInterceptor


class FirewallRestTransport(FirewallTransport):
    """REST backend transport for Firewall.

    Firewall resources are used to define a collection of access
    control rules for an Application. Each rule is defined with a
    position which specifies the rule's order in the sequence of
    rules, an IP range to be matched against requests, and an action
    to take upon matching requests.

    Every request is evaluated against the Firewall rules in
    priority order. Processesing stops at the first rule which
    matches the request's IP address. A final rule always specifies
    an action that applies to all remaining IP addresses. The
    default final rule for a newly-created application will be set
    to "allow" if not otherwise specified by the user.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "appengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[FirewallRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'appengine.googleapis.com').
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
        self._interceptor = interceptor or FirewallRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchUpdateIngressRules(FirewallRestStub):
        def __hash__(self):
            return hash("BatchUpdateIngressRules")

        def __call__(
            self,
            request: appengine.BatchUpdateIngressRulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> appengine.BatchUpdateIngressRulesResponse:
            r"""Call the batch update ingress
            rules method over HTTP.

                Args:
                    request (~.appengine.BatchUpdateIngressRulesRequest):
                        The request object. Request message for
                    ``Firewall.BatchUpdateIngressRules``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.appengine.BatchUpdateIngressRulesResponse:
                        Response message for ``Firewall.UpdateAllIngressRules``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=apps/*/firewall/ingressRules}:batchUpdate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_update_ingress_rules(
                request, metadata
            )
            pb_request = appengine.BatchUpdateIngressRulesRequest.pb(request)
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
            resp = appengine.BatchUpdateIngressRulesResponse()
            pb_resp = appengine.BatchUpdateIngressRulesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_update_ingress_rules(resp)
            return resp

    class _CreateIngressRule(FirewallRestStub):
        def __hash__(self):
            return hash("CreateIngressRule")

        def __call__(
            self,
            request: appengine.CreateIngressRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firewall.FirewallRule:
            r"""Call the create ingress rule method over HTTP.

            Args:
                request (~.appengine.CreateIngressRuleRequest):
                    The request object. Request message for ``Firewall.CreateIngressRule``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firewall.FirewallRule:
                    A single firewall rule that is
                evaluated against incoming traffic and
                provides an action to take on matched
                requests.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=apps/*}/firewall/ingressRules",
                    "body": "rule",
                },
            ]
            request, metadata = self._interceptor.pre_create_ingress_rule(
                request, metadata
            )
            pb_request = appengine.CreateIngressRuleRequest.pb(request)
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
            resp = firewall.FirewallRule()
            pb_resp = firewall.FirewallRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_ingress_rule(resp)
            return resp

    class _DeleteIngressRule(FirewallRestStub):
        def __hash__(self):
            return hash("DeleteIngressRule")

        def __call__(
            self,
            request: appengine.DeleteIngressRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete ingress rule method over HTTP.

            Args:
                request (~.appengine.DeleteIngressRuleRequest):
                    The request object. Request message for ``Firewall.DeleteIngressRule``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=apps/*/firewall/ingressRules/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_ingress_rule(
                request, metadata
            )
            pb_request = appengine.DeleteIngressRuleRequest.pb(request)
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

    class _GetIngressRule(FirewallRestStub):
        def __hash__(self):
            return hash("GetIngressRule")

        def __call__(
            self,
            request: appengine.GetIngressRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firewall.FirewallRule:
            r"""Call the get ingress rule method over HTTP.

            Args:
                request (~.appengine.GetIngressRuleRequest):
                    The request object. Request message for ``Firewall.GetIngressRule``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firewall.FirewallRule:
                    A single firewall rule that is
                evaluated against incoming traffic and
                provides an action to take on matched
                requests.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=apps/*/firewall/ingressRules/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_ingress_rule(
                request, metadata
            )
            pb_request = appengine.GetIngressRuleRequest.pb(request)
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
            resp = firewall.FirewallRule()
            pb_resp = firewall.FirewallRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_ingress_rule(resp)
            return resp

    class _ListIngressRules(FirewallRestStub):
        def __hash__(self):
            return hash("ListIngressRules")

        def __call__(
            self,
            request: appengine.ListIngressRulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> appengine.ListIngressRulesResponse:
            r"""Call the list ingress rules method over HTTP.

            Args:
                request (~.appengine.ListIngressRulesRequest):
                    The request object. Request message for ``Firewall.ListIngressRules``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.appengine.ListIngressRulesResponse:
                    Response message for ``Firewall.ListIngressRules``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=apps/*}/firewall/ingressRules",
                },
            ]
            request, metadata = self._interceptor.pre_list_ingress_rules(
                request, metadata
            )
            pb_request = appengine.ListIngressRulesRequest.pb(request)
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
            resp = appengine.ListIngressRulesResponse()
            pb_resp = appengine.ListIngressRulesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_ingress_rules(resp)
            return resp

    class _UpdateIngressRule(FirewallRestStub):
        def __hash__(self):
            return hash("UpdateIngressRule")

        def __call__(
            self,
            request: appengine.UpdateIngressRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firewall.FirewallRule:
            r"""Call the update ingress rule method over HTTP.

            Args:
                request (~.appengine.UpdateIngressRuleRequest):
                    The request object. Request message for ``Firewall.UpdateIngressRule``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firewall.FirewallRule:
                    A single firewall rule that is
                evaluated against incoming traffic and
                provides an action to take on matched
                requests.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{name=apps/*/firewall/ingressRules/*}",
                    "body": "rule",
                },
            ]
            request, metadata = self._interceptor.pre_update_ingress_rule(
                request, metadata
            )
            pb_request = appengine.UpdateIngressRuleRequest.pb(request)
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
            resp = firewall.FirewallRule()
            pb_resp = firewall.FirewallRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_ingress_rule(resp)
            return resp

    @property
    def batch_update_ingress_rules(
        self,
    ) -> Callable[
        [appengine.BatchUpdateIngressRulesRequest],
        appengine.BatchUpdateIngressRulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateIngressRules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_ingress_rule(
        self,
    ) -> Callable[[appengine.CreateIngressRuleRequest], firewall.FirewallRule]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateIngressRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_ingress_rule(
        self,
    ) -> Callable[[appengine.DeleteIngressRuleRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteIngressRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_ingress_rule(
        self,
    ) -> Callable[[appengine.GetIngressRuleRequest], firewall.FirewallRule]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIngressRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_ingress_rules(
        self,
    ) -> Callable[
        [appengine.ListIngressRulesRequest], appengine.ListIngressRulesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListIngressRules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_ingress_rule(
        self,
    ) -> Callable[[appengine.UpdateIngressRuleRequest], firewall.FirewallRule]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateIngressRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("FirewallRestTransport",)
