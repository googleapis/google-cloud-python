# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.billing.budgets_v1.types import budget_model, budget_service

from .base import BudgetServiceTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class BudgetServiceRestInterceptor:
    """Interceptor for BudgetService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BudgetServiceRestTransport.

    .. code-block:: python
        class MyCustomBudgetServiceInterceptor(BudgetServiceRestInterceptor):
            def pre_create_budget(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_budget(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_budget(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_budget(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_budget(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_budgets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_budgets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_budget(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_budget(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BudgetServiceRestTransport(interceptor=MyCustomBudgetServiceInterceptor())
        client = BudgetServiceClient(transport=transport)


    """

    def pre_create_budget(
        self,
        request: budget_service.CreateBudgetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[budget_service.CreateBudgetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_budget

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BudgetService server.
        """
        return request, metadata

    def post_create_budget(self, response: budget_model.Budget) -> budget_model.Budget:
        """Post-rpc interceptor for create_budget

        Override in a subclass to manipulate the response
        after it is returned by the BudgetService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_budget(
        self,
        request: budget_service.DeleteBudgetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[budget_service.DeleteBudgetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_budget

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BudgetService server.
        """
        return request, metadata

    def pre_get_budget(
        self,
        request: budget_service.GetBudgetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[budget_service.GetBudgetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_budget

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BudgetService server.
        """
        return request, metadata

    def post_get_budget(self, response: budget_model.Budget) -> budget_model.Budget:
        """Post-rpc interceptor for get_budget

        Override in a subclass to manipulate the response
        after it is returned by the BudgetService server but before
        it is returned to user code.
        """
        return response

    def pre_list_budgets(
        self,
        request: budget_service.ListBudgetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[budget_service.ListBudgetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_budgets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BudgetService server.
        """
        return request, metadata

    def post_list_budgets(
        self, response: budget_service.ListBudgetsResponse
    ) -> budget_service.ListBudgetsResponse:
        """Post-rpc interceptor for list_budgets

        Override in a subclass to manipulate the response
        after it is returned by the BudgetService server but before
        it is returned to user code.
        """
        return response

    def pre_update_budget(
        self,
        request: budget_service.UpdateBudgetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[budget_service.UpdateBudgetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_budget

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BudgetService server.
        """
        return request, metadata

    def post_update_budget(self, response: budget_model.Budget) -> budget_model.Budget:
        """Post-rpc interceptor for update_budget

        Override in a subclass to manipulate the response
        after it is returned by the BudgetService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BudgetServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BudgetServiceRestInterceptor


class BudgetServiceRestTransport(BudgetServiceTransport):
    """REST backend transport for BudgetService.

    BudgetService stores Cloud Billing budgets, which define a
    budget plan and rules to execute as we track spend against that
    plan.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "billingbudgets.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BudgetServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
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
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or BudgetServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateBudget(BudgetServiceRestStub):
        def __hash__(self):
            return hash("CreateBudget")

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
            request: budget_service.CreateBudgetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> budget_model.Budget:
            r"""Call the create budget method over HTTP.

            Args:
                request (~.budget_service.CreateBudgetRequest):
                    The request object. Request for CreateBudget
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.budget_model.Budget:
                    A budget is a plan that describes
                what you expect to spend on Cloud
                projects, plus the rules to execute as
                spend is tracked against that plan, (for
                example, send an alert when 90% of the
                target spend is met). The budget time
                period is configurable, with options
                such as month (default), quarter, year,
                or custom time period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=billingAccounts/*}/budgets",
                    "body": "budget",
                },
            ]
            request, metadata = self._interceptor.pre_create_budget(request, metadata)
            pb_request = budget_service.CreateBudgetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = budget_model.Budget()
            pb_resp = budget_model.Budget.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_budget(resp)
            return resp

    class _DeleteBudget(BudgetServiceRestStub):
        def __hash__(self):
            return hash("DeleteBudget")

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
            request: budget_service.DeleteBudgetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete budget method over HTTP.

            Args:
                request (~.budget_service.DeleteBudgetRequest):
                    The request object. Request for DeleteBudget
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=billingAccounts/*/budgets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_budget(request, metadata)
            pb_request = budget_service.DeleteBudgetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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

    class _GetBudget(BudgetServiceRestStub):
        def __hash__(self):
            return hash("GetBudget")

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
            request: budget_service.GetBudgetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> budget_model.Budget:
            r"""Call the get budget method over HTTP.

            Args:
                request (~.budget_service.GetBudgetRequest):
                    The request object. Request for GetBudget
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.budget_model.Budget:
                    A budget is a plan that describes
                what you expect to spend on Cloud
                projects, plus the rules to execute as
                spend is tracked against that plan, (for
                example, send an alert when 90% of the
                target spend is met). The budget time
                period is configurable, with options
                such as month (default), quarter, year,
                or custom time period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=billingAccounts/*/budgets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_budget(request, metadata)
            pb_request = budget_service.GetBudgetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = budget_model.Budget()
            pb_resp = budget_model.Budget.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_budget(resp)
            return resp

    class _ListBudgets(BudgetServiceRestStub):
        def __hash__(self):
            return hash("ListBudgets")

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
            request: budget_service.ListBudgetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> budget_service.ListBudgetsResponse:
            r"""Call the list budgets method over HTTP.

            Args:
                request (~.budget_service.ListBudgetsRequest):
                    The request object. Request for ListBudgets
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.budget_service.ListBudgetsResponse:
                    Response for ListBudgets
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=billingAccounts/*}/budgets",
                },
            ]
            request, metadata = self._interceptor.pre_list_budgets(request, metadata)
            pb_request = budget_service.ListBudgetsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = budget_service.ListBudgetsResponse()
            pb_resp = budget_service.ListBudgetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_budgets(resp)
            return resp

    class _UpdateBudget(BudgetServiceRestStub):
        def __hash__(self):
            return hash("UpdateBudget")

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
            request: budget_service.UpdateBudgetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> budget_model.Budget:
            r"""Call the update budget method over HTTP.

            Args:
                request (~.budget_service.UpdateBudgetRequest):
                    The request object. Request for UpdateBudget
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.budget_model.Budget:
                    A budget is a plan that describes
                what you expect to spend on Cloud
                projects, plus the rules to execute as
                spend is tracked against that plan, (for
                example, send an alert when 90% of the
                target spend is met). The budget time
                period is configurable, with options
                such as month (default), quarter, year,
                or custom time period.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{budget.name=billingAccounts/*/budgets/*}",
                    "body": "budget",
                },
            ]
            request, metadata = self._interceptor.pre_update_budget(request, metadata)
            pb_request = budget_service.UpdateBudgetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = budget_model.Budget()
            pb_resp = budget_model.Budget.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_budget(resp)
            return resp

    @property
    def create_budget(
        self,
    ) -> Callable[[budget_service.CreateBudgetRequest], budget_model.Budget]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBudget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_budget(
        self,
    ) -> Callable[[budget_service.DeleteBudgetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBudget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_budget(
        self,
    ) -> Callable[[budget_service.GetBudgetRequest], budget_model.Budget]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBudget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_budgets(
        self,
    ) -> Callable[
        [budget_service.ListBudgetsRequest], budget_service.ListBudgetsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBudgets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_budget(
        self,
    ) -> Callable[[budget_service.UpdateBudgetRequest], budget_model.Budget]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBudget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BudgetServiceRestTransport",)
