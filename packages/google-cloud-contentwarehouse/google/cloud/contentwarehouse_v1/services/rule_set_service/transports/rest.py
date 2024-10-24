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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.contentwarehouse_v1.types import rule_engine, ruleset_service_request

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseRuleSetServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RuleSetServiceRestInterceptor:
    """Interceptor for RuleSetService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RuleSetServiceRestTransport.

    .. code-block:: python
        class MyCustomRuleSetServiceInterceptor(RuleSetServiceRestInterceptor):
            def pre_create_rule_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_rule_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_rule_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_rule_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_rule_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_rule_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_rule_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_rule_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_rule_set(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RuleSetServiceRestTransport(interceptor=MyCustomRuleSetServiceInterceptor())
        client = RuleSetServiceClient(transport=transport)


    """

    def pre_create_rule_set(
        self,
        request: ruleset_service_request.CreateRuleSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ruleset_service_request.CreateRuleSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_rule_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuleSetService server.
        """
        return request, metadata

    def post_create_rule_set(
        self, response: rule_engine.RuleSet
    ) -> rule_engine.RuleSet:
        """Post-rpc interceptor for create_rule_set

        Override in a subclass to manipulate the response
        after it is returned by the RuleSetService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_rule_set(
        self,
        request: ruleset_service_request.DeleteRuleSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ruleset_service_request.DeleteRuleSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_rule_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuleSetService server.
        """
        return request, metadata

    def pre_get_rule_set(
        self,
        request: ruleset_service_request.GetRuleSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ruleset_service_request.GetRuleSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_rule_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuleSetService server.
        """
        return request, metadata

    def post_get_rule_set(self, response: rule_engine.RuleSet) -> rule_engine.RuleSet:
        """Post-rpc interceptor for get_rule_set

        Override in a subclass to manipulate the response
        after it is returned by the RuleSetService server but before
        it is returned to user code.
        """
        return response

    def pre_list_rule_sets(
        self,
        request: ruleset_service_request.ListRuleSetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ruleset_service_request.ListRuleSetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_rule_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuleSetService server.
        """
        return request, metadata

    def post_list_rule_sets(
        self, response: ruleset_service_request.ListRuleSetsResponse
    ) -> ruleset_service_request.ListRuleSetsResponse:
        """Post-rpc interceptor for list_rule_sets

        Override in a subclass to manipulate the response
        after it is returned by the RuleSetService server but before
        it is returned to user code.
        """
        return response

    def pre_update_rule_set(
        self,
        request: ruleset_service_request.UpdateRuleSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[ruleset_service_request.UpdateRuleSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_rule_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuleSetService server.
        """
        return request, metadata

    def post_update_rule_set(
        self, response: rule_engine.RuleSet
    ) -> rule_engine.RuleSet:
        """Post-rpc interceptor for update_rule_set

        Override in a subclass to manipulate the response
        after it is returned by the RuleSetService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RuleSetService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the RuleSetService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RuleSetServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RuleSetServiceRestInterceptor


class RuleSetServiceRestTransport(_BaseRuleSetServiceRestTransport):
    """REST backend synchronous transport for RuleSetService.

    Service to manage customer specific RuleSets.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "contentwarehouse.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RuleSetServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'contentwarehouse.googleapis.com').
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
        self._interceptor = interceptor or RuleSetServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateRuleSet(
        _BaseRuleSetServiceRestTransport._BaseCreateRuleSet, RuleSetServiceRestStub
    ):
        def __hash__(self):
            return hash("RuleSetServiceRestTransport.CreateRuleSet")

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
            request: ruleset_service_request.CreateRuleSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rule_engine.RuleSet:
            r"""Call the create rule set method over HTTP.

            Args:
                request (~.ruleset_service_request.CreateRuleSetRequest):
                    The request object. Request message for
                RuleSetService.CreateRuleSet.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.rule_engine.RuleSet:
                    Represents a set of rules from a
                single customer.

            """

            http_options = (
                _BaseRuleSetServiceRestTransport._BaseCreateRuleSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_rule_set(request, metadata)
            transcoded_request = _BaseRuleSetServiceRestTransport._BaseCreateRuleSet._get_transcoded_request(
                http_options, request
            )

            body = _BaseRuleSetServiceRestTransport._BaseCreateRuleSet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRuleSetServiceRestTransport._BaseCreateRuleSet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RuleSetServiceRestTransport._CreateRuleSet._get_response(
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
            resp = rule_engine.RuleSet()
            pb_resp = rule_engine.RuleSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_rule_set(resp)
            return resp

    class _DeleteRuleSet(
        _BaseRuleSetServiceRestTransport._BaseDeleteRuleSet, RuleSetServiceRestStub
    ):
        def __hash__(self):
            return hash("RuleSetServiceRestTransport.DeleteRuleSet")

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
            request: ruleset_service_request.DeleteRuleSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete rule set method over HTTP.

            Args:
                request (~.ruleset_service_request.DeleteRuleSetRequest):
                    The request object. Request message for
                RuleSetService.DeleteRuleSet.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseRuleSetServiceRestTransport._BaseDeleteRuleSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_rule_set(request, metadata)
            transcoded_request = _BaseRuleSetServiceRestTransport._BaseDeleteRuleSet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRuleSetServiceRestTransport._BaseDeleteRuleSet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RuleSetServiceRestTransport._DeleteRuleSet._get_response(
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

    class _GetRuleSet(
        _BaseRuleSetServiceRestTransport._BaseGetRuleSet, RuleSetServiceRestStub
    ):
        def __hash__(self):
            return hash("RuleSetServiceRestTransport.GetRuleSet")

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
            request: ruleset_service_request.GetRuleSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rule_engine.RuleSet:
            r"""Call the get rule set method over HTTP.

            Args:
                request (~.ruleset_service_request.GetRuleSetRequest):
                    The request object. Request message for
                RuleSetService.GetRuleSet.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.rule_engine.RuleSet:
                    Represents a set of rules from a
                single customer.

            """

            http_options = (
                _BaseRuleSetServiceRestTransport._BaseGetRuleSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_rule_set(request, metadata)
            transcoded_request = _BaseRuleSetServiceRestTransport._BaseGetRuleSet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseRuleSetServiceRestTransport._BaseGetRuleSet._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RuleSetServiceRestTransport._GetRuleSet._get_response(
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
            resp = rule_engine.RuleSet()
            pb_resp = rule_engine.RuleSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_rule_set(resp)
            return resp

    class _ListRuleSets(
        _BaseRuleSetServiceRestTransport._BaseListRuleSets, RuleSetServiceRestStub
    ):
        def __hash__(self):
            return hash("RuleSetServiceRestTransport.ListRuleSets")

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
            request: ruleset_service_request.ListRuleSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ruleset_service_request.ListRuleSetsResponse:
            r"""Call the list rule sets method over HTTP.

            Args:
                request (~.ruleset_service_request.ListRuleSetsRequest):
                    The request object. Request message for
                RuleSetService.ListRuleSets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ruleset_service_request.ListRuleSetsResponse:
                    Response message for
                RuleSetService.ListRuleSets.

            """

            http_options = (
                _BaseRuleSetServiceRestTransport._BaseListRuleSets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_rule_sets(request, metadata)
            transcoded_request = _BaseRuleSetServiceRestTransport._BaseListRuleSets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRuleSetServiceRestTransport._BaseListRuleSets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RuleSetServiceRestTransport._ListRuleSets._get_response(
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
            resp = ruleset_service_request.ListRuleSetsResponse()
            pb_resp = ruleset_service_request.ListRuleSetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_rule_sets(resp)
            return resp

    class _UpdateRuleSet(
        _BaseRuleSetServiceRestTransport._BaseUpdateRuleSet, RuleSetServiceRestStub
    ):
        def __hash__(self):
            return hash("RuleSetServiceRestTransport.UpdateRuleSet")

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
            request: ruleset_service_request.UpdateRuleSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rule_engine.RuleSet:
            r"""Call the update rule set method over HTTP.

            Args:
                request (~.ruleset_service_request.UpdateRuleSetRequest):
                    The request object. Request message for
                RuleSetService.UpdateRuleSet.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.rule_engine.RuleSet:
                    Represents a set of rules from a
                single customer.

            """

            http_options = (
                _BaseRuleSetServiceRestTransport._BaseUpdateRuleSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_rule_set(request, metadata)
            transcoded_request = _BaseRuleSetServiceRestTransport._BaseUpdateRuleSet._get_transcoded_request(
                http_options, request
            )

            body = _BaseRuleSetServiceRestTransport._BaseUpdateRuleSet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRuleSetServiceRestTransport._BaseUpdateRuleSet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RuleSetServiceRestTransport._UpdateRuleSet._get_response(
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
            resp = rule_engine.RuleSet()
            pb_resp = rule_engine.RuleSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_rule_set(resp)
            return resp

    @property
    def create_rule_set(
        self,
    ) -> Callable[[ruleset_service_request.CreateRuleSetRequest], rule_engine.RuleSet]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRuleSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_rule_set(
        self,
    ) -> Callable[[ruleset_service_request.DeleteRuleSetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRuleSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_rule_set(
        self,
    ) -> Callable[[ruleset_service_request.GetRuleSetRequest], rule_engine.RuleSet]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRuleSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_rule_sets(
        self,
    ) -> Callable[
        [ruleset_service_request.ListRuleSetsRequest],
        ruleset_service_request.ListRuleSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRuleSets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_rule_set(
        self,
    ) -> Callable[[ruleset_service_request.UpdateRuleSetRequest], rule_engine.RuleSet]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRuleSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseRuleSetServiceRestTransport._BaseGetOperation, RuleSetServiceRestStub
    ):
        def __hash__(self):
            return hash("RuleSetServiceRestTransport.GetOperation")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseRuleSetServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseRuleSetServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRuleSetServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = RuleSetServiceRestTransport._GetOperation._get_response(
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
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RuleSetServiceRestTransport",)
