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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.bigquery_datapolicies_v1.types import datapolicy

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDataPolicyServiceRestTransport

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


class DataPolicyServiceRestInterceptor:
    """Interceptor for DataPolicyService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DataPolicyServiceRestTransport.

    .. code-block:: python
        class MyCustomDataPolicyServiceInterceptor(DataPolicyServiceRestInterceptor):
            def pre_create_data_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_data_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_data_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_data_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_data_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rename_data_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rename_data_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DataPolicyServiceRestTransport(interceptor=MyCustomDataPolicyServiceInterceptor())
        client = DataPolicyServiceClient(transport=transport)


    """

    def pre_create_data_policy(
        self,
        request: datapolicy.CreateDataPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        datapolicy.CreateDataPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_data_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_create_data_policy(
        self, response: datapolicy.DataPolicy
    ) -> datapolicy.DataPolicy:
        """Post-rpc interceptor for create_data_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_data_policy(
        self,
        request: datapolicy.DeleteDataPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        datapolicy.DeleteDataPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_data_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def pre_get_data_policy(
        self,
        request: datapolicy.GetDataPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        datapolicy.GetDataPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_data_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_get_data_policy(
        self, response: datapolicy.DataPolicy
    ) -> datapolicy.DataPolicy:
        """Post-rpc interceptor for get_data_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_list_data_policies(
        self,
        request: datapolicy.ListDataPoliciesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        datapolicy.ListDataPoliciesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_data_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_list_data_policies(
        self, response: datapolicy.ListDataPoliciesResponse
    ) -> datapolicy.ListDataPoliciesResponse:
        """Post-rpc interceptor for list_data_policies

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_rename_data_policy(
        self,
        request: datapolicy.RenameDataPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        datapolicy.RenameDataPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for rename_data_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_rename_data_policy(
        self, response: datapolicy.DataPolicy
    ) -> datapolicy.DataPolicy:
        """Post-rpc interceptor for rename_data_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.TestIamPermissionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response

    def pre_update_data_policy(
        self,
        request: datapolicy.UpdateDataPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        datapolicy.UpdateDataPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_data_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataPolicyService server.
        """
        return request, metadata

    def post_update_data_policy(
        self, response: datapolicy.DataPolicy
    ) -> datapolicy.DataPolicy:
        """Post-rpc interceptor for update_data_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataPolicyService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DataPolicyServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataPolicyServiceRestInterceptor


class DataPolicyServiceRestTransport(_BaseDataPolicyServiceRestTransport):
    """REST backend synchronous transport for DataPolicyService.

    Data Policy Service provides APIs for managing the
    label-policy bindings.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "bigquerydatapolicy.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DataPolicyServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigquerydatapolicy.googleapis.com').
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
        self._interceptor = interceptor or DataPolicyServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDataPolicy(
        _BaseDataPolicyServiceRestTransport._BaseCreateDataPolicy,
        DataPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.CreateDataPolicy")

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
            request: datapolicy.CreateDataPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> datapolicy.DataPolicy:
            r"""Call the create data policy method over HTTP.

            Args:
                request (~.datapolicy.CreateDataPolicyRequest):
                    The request object. Request message for the
                CreateDataPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.datapolicy.DataPolicy:
                    Represents the label-policy binding.
            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseCreateDataPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_data_policy(
                request, metadata
            )
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseCreateDataPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataPolicyServiceRestTransport._BaseCreateDataPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseCreateDataPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.CreateDataPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "CreateDataPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._CreateDataPolicy._get_response(
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
            resp = datapolicy.DataPolicy()
            pb_resp = datapolicy.DataPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_data_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = datapolicy.DataPolicy.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.create_data_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "CreateDataPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteDataPolicy(
        _BaseDataPolicyServiceRestTransport._BaseDeleteDataPolicy,
        DataPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.DeleteDataPolicy")

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
            request: datapolicy.DeleteDataPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete data policy method over HTTP.

            Args:
                request (~.datapolicy.DeleteDataPolicyRequest):
                    The request object. Request message for the
                DeleteDataPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseDeleteDataPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_data_policy(
                request, metadata
            )
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseDeleteDataPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseDeleteDataPolicy._get_query_params_json(
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
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.DeleteDataPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "DeleteDataPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._DeleteDataPolicy._get_response(
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

    class _GetDataPolicy(
        _BaseDataPolicyServiceRestTransport._BaseGetDataPolicy,
        DataPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.GetDataPolicy")

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
            request: datapolicy.GetDataPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> datapolicy.DataPolicy:
            r"""Call the get data policy method over HTTP.

            Args:
                request (~.datapolicy.GetDataPolicyRequest):
                    The request object. Request message for the GetDataPolicy
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.datapolicy.DataPolicy:
                    Represents the label-policy binding.
            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseGetDataPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_data_policy(request, metadata)
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseGetDataPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseGetDataPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.GetDataPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "GetDataPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._GetDataPolicy._get_response(
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
            resp = datapolicy.DataPolicy()
            pb_resp = datapolicy.DataPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_data_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = datapolicy.DataPolicy.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.get_data_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "GetDataPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetIamPolicy(
        _BaseDataPolicyServiceRestTransport._BaseGetIamPolicy, DataPolicyServiceRestStub
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseGetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataPolicyServiceRestTransport._BaseGetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseGetIamPolicy._get_query_params_json(
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
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "GetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.get_iam_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "GetIamPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDataPolicies(
        _BaseDataPolicyServiceRestTransport._BaseListDataPolicies,
        DataPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.ListDataPolicies")

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
            request: datapolicy.ListDataPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> datapolicy.ListDataPoliciesResponse:
            r"""Call the list data policies method over HTTP.

            Args:
                request (~.datapolicy.ListDataPoliciesRequest):
                    The request object. Request message for the
                ListDataPolicies method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.datapolicy.ListDataPoliciesResponse:
                    Response message for the
                ListDataPolicies method.

            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseListDataPolicies._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_data_policies(
                request, metadata
            )
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseListDataPolicies._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseListDataPolicies._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.ListDataPolicies",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "ListDataPolicies",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._ListDataPolicies._get_response(
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
            resp = datapolicy.ListDataPoliciesResponse()
            pb_resp = datapolicy.ListDataPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_data_policies(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = datapolicy.ListDataPoliciesResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.list_data_policies",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "ListDataPolicies",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RenameDataPolicy(
        _BaseDataPolicyServiceRestTransport._BaseRenameDataPolicy,
        DataPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.RenameDataPolicy")

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
            request: datapolicy.RenameDataPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> datapolicy.DataPolicy:
            r"""Call the rename data policy method over HTTP.

            Args:
                request (~.datapolicy.RenameDataPolicyRequest):
                    The request object. Request message for the
                RenameDataPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.datapolicy.DataPolicy:
                    Represents the label-policy binding.
            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseRenameDataPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_rename_data_policy(
                request, metadata
            )
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseRenameDataPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataPolicyServiceRestTransport._BaseRenameDataPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseRenameDataPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.RenameDataPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "RenameDataPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._RenameDataPolicy._get_response(
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
            resp = datapolicy.DataPolicy()
            pb_resp = datapolicy.DataPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_rename_data_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = datapolicy.DataPolicy.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.rename_data_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "RenameDataPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SetIamPolicy(
        _BaseDataPolicyServiceRestTransport._BaseSetIamPolicy, DataPolicyServiceRestStub
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseSetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataPolicyServiceRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseSetIamPolicy._get_query_params_json(
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
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "SetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._SetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_set_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.set_iam_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "SetIamPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _TestIamPermissions(
        _BaseDataPolicyServiceRestTransport._BaseTestIamPermissions,
        DataPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseTestIamPermissions._get_http_options()
            )

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataPolicyServiceRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseTestIamPermissions._get_query_params_json(
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
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._TestIamPermissions._get_response(
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_test_iam_permissions(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.test_iam_permissions",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "TestIamPermissions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateDataPolicy(
        _BaseDataPolicyServiceRestTransport._BaseUpdateDataPolicy,
        DataPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataPolicyServiceRestTransport.UpdateDataPolicy")

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
            request: datapolicy.UpdateDataPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> datapolicy.DataPolicy:
            r"""Call the update data policy method over HTTP.

            Args:
                request (~.datapolicy.UpdateDataPolicyRequest):
                    The request object. Response message for the
                UpdateDataPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.datapolicy.DataPolicy:
                    Represents the label-policy binding.
            """

            http_options = (
                _BaseDataPolicyServiceRestTransport._BaseUpdateDataPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_data_policy(
                request, metadata
            )
            transcoded_request = _BaseDataPolicyServiceRestTransport._BaseUpdateDataPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataPolicyServiceRestTransport._BaseUpdateDataPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataPolicyServiceRestTransport._BaseUpdateDataPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.UpdateDataPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "UpdateDataPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataPolicyServiceRestTransport._UpdateDataPolicy._get_response(
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
            resp = datapolicy.DataPolicy()
            pb_resp = datapolicy.DataPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_data_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = datapolicy.DataPolicy.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery.datapolicies_v1.DataPolicyServiceClient.update_data_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.datapolicies.v1.DataPolicyService",
                        "rpcName": "UpdateDataPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_data_policy(
        self,
    ) -> Callable[[datapolicy.CreateDataPolicyRequest], datapolicy.DataPolicy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_data_policy(
        self,
    ) -> Callable[[datapolicy.DeleteDataPolicyRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_policy(
        self,
    ) -> Callable[[datapolicy.GetDataPolicyRequest], datapolicy.DataPolicy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_data_policies(
        self,
    ) -> Callable[
        [datapolicy.ListDataPoliciesRequest], datapolicy.ListDataPoliciesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDataPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rename_data_policy(
        self,
    ) -> Callable[[datapolicy.RenameDataPolicyRequest], datapolicy.DataPolicy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RenameDataPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_data_policy(
        self,
    ) -> Callable[[datapolicy.UpdateDataPolicyRequest], datapolicy.DataPolicy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DataPolicyServiceRestTransport",)
