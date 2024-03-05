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

from google.cloud.binaryauthorization_v1beta1.types import resources, service

from .base import BinauthzManagementServiceV1Beta1Transport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class BinauthzManagementServiceV1Beta1RestInterceptor:
    """Interceptor for BinauthzManagementServiceV1Beta1.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BinauthzManagementServiceV1Beta1RestTransport.

    .. code-block:: python
        class MyCustomBinauthzManagementServiceV1Beta1Interceptor(BinauthzManagementServiceV1Beta1RestInterceptor):
            def pre_create_attestor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_attestor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_attestor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_attestor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_attestor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_attestors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_attestors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_attestor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_attestor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BinauthzManagementServiceV1Beta1RestTransport(interceptor=MyCustomBinauthzManagementServiceV1Beta1Interceptor())
        client = BinauthzManagementServiceV1Beta1Client(transport=transport)


    """

    def pre_create_attestor(
        self,
        request: service.CreateAttestorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateAttestorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_attestor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BinauthzManagementServiceV1Beta1 server.
        """
        return request, metadata

    def post_create_attestor(self, response: resources.Attestor) -> resources.Attestor:
        """Post-rpc interceptor for create_attestor

        Override in a subclass to manipulate the response
        after it is returned by the BinauthzManagementServiceV1Beta1 server but before
        it is returned to user code.
        """
        return response

    def pre_delete_attestor(
        self,
        request: service.DeleteAttestorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DeleteAttestorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_attestor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BinauthzManagementServiceV1Beta1 server.
        """
        return request, metadata

    def pre_get_attestor(
        self, request: service.GetAttestorRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetAttestorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_attestor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BinauthzManagementServiceV1Beta1 server.
        """
        return request, metadata

    def post_get_attestor(self, response: resources.Attestor) -> resources.Attestor:
        """Post-rpc interceptor for get_attestor

        Override in a subclass to manipulate the response
        after it is returned by the BinauthzManagementServiceV1Beta1 server but before
        it is returned to user code.
        """
        return response

    def pre_get_policy(
        self, request: service.GetPolicyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BinauthzManagementServiceV1Beta1 server.
        """
        return request, metadata

    def post_get_policy(self, response: resources.Policy) -> resources.Policy:
        """Post-rpc interceptor for get_policy

        Override in a subclass to manipulate the response
        after it is returned by the BinauthzManagementServiceV1Beta1 server but before
        it is returned to user code.
        """
        return response

    def pre_list_attestors(
        self, request: service.ListAttestorsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListAttestorsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_attestors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BinauthzManagementServiceV1Beta1 server.
        """
        return request, metadata

    def post_list_attestors(
        self, response: service.ListAttestorsResponse
    ) -> service.ListAttestorsResponse:
        """Post-rpc interceptor for list_attestors

        Override in a subclass to manipulate the response
        after it is returned by the BinauthzManagementServiceV1Beta1 server but before
        it is returned to user code.
        """
        return response

    def pre_update_attestor(
        self,
        request: service.UpdateAttestorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateAttestorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_attestor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BinauthzManagementServiceV1Beta1 server.
        """
        return request, metadata

    def post_update_attestor(self, response: resources.Attestor) -> resources.Attestor:
        """Post-rpc interceptor for update_attestor

        Override in a subclass to manipulate the response
        after it is returned by the BinauthzManagementServiceV1Beta1 server but before
        it is returned to user code.
        """
        return response

    def pre_update_policy(
        self, request: service.UpdatePolicyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdatePolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BinauthzManagementServiceV1Beta1 server.
        """
        return request, metadata

    def post_update_policy(self, response: resources.Policy) -> resources.Policy:
        """Post-rpc interceptor for update_policy

        Override in a subclass to manipulate the response
        after it is returned by the BinauthzManagementServiceV1Beta1 server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BinauthzManagementServiceV1Beta1RestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BinauthzManagementServiceV1Beta1RestInterceptor


class BinauthzManagementServiceV1Beta1RestTransport(
    BinauthzManagementServiceV1Beta1Transport
):
    """REST backend transport for BinauthzManagementServiceV1Beta1.

    Google Cloud Management Service for Binary Authorization admission
    policies and attestation authorities.

    This API implements a REST model with the following objects:

    -  [Policy][google.cloud.binaryauthorization.v1beta1.Policy]
    -  [Attestor][google.cloud.binaryauthorization.v1beta1.Attestor]

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "binaryauthorization.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BinauthzManagementServiceV1Beta1RestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'binaryauthorization.googleapis.com').
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
        self._interceptor = (
            interceptor or BinauthzManagementServiceV1Beta1RestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    class _CreateAttestor(BinauthzManagementServiceV1Beta1RestStub):
        def __hash__(self):
            return hash("CreateAttestor")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "attestorId": "",
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
            request: service.CreateAttestorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Attestor:
            r"""Call the create attestor method over HTTP.

            Args:
                request (~.service.CreateAttestorRequest):
                    The request object. Request message for
                [BinauthzManagementService.CreateAttestor][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Attestor:
                    An
                [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
                that attests to container image artifacts. An existing
                attestor cannot be modified except where indicated.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{parent=projects/*}/attestors",
                    "body": "attestor",
                },
            ]
            request, metadata = self._interceptor.pre_create_attestor(request, metadata)
            pb_request = service.CreateAttestorRequest.pb(request)
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
            resp = resources.Attestor()
            pb_resp = resources.Attestor.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_attestor(resp)
            return resp

    class _DeleteAttestor(BinauthzManagementServiceV1Beta1RestStub):
        def __hash__(self):
            return hash("DeleteAttestor")

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
            request: service.DeleteAttestorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete attestor method over HTTP.

            Args:
                request (~.service.DeleteAttestorRequest):
                    The request object. Request message for
                [BinauthzManagementService.DeleteAttestor][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta1/{name=projects/*/attestors/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_attestor(request, metadata)
            pb_request = service.DeleteAttestorRequest.pb(request)
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

    class _GetAttestor(BinauthzManagementServiceV1Beta1RestStub):
        def __hash__(self):
            return hash("GetAttestor")

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
            request: service.GetAttestorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Attestor:
            r"""Call the get attestor method over HTTP.

            Args:
                request (~.service.GetAttestorRequest):
                    The request object. Request message for
                [BinauthzManagementService.GetAttestor][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Attestor:
                    An
                [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
                that attests to container image artifacts. An existing
                attestor cannot be modified except where indicated.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/attestors/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_attestor(request, metadata)
            pb_request = service.GetAttestorRequest.pb(request)
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
            resp = resources.Attestor()
            pb_resp = resources.Attestor.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_attestor(resp)
            return resp

    class _GetPolicy(BinauthzManagementServiceV1Beta1RestStub):
        def __hash__(self):
            return hash("GetPolicy")

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
            request: service.GetPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Policy:
            r"""Call the get policy method over HTTP.

            Args:
                request (~.service.GetPolicyRequest):
                    The request object. Request message for
                [BinauthzManagementService.GetPolicy][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Policy:
                    A
                [policy][google.cloud.binaryauthorization.v1beta1.Policy]
                for Binary Authorization.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/policy}",
                },
            ]
            request, metadata = self._interceptor.pre_get_policy(request, metadata)
            pb_request = service.GetPolicyRequest.pb(request)
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
            resp = resources.Policy()
            pb_resp = resources.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_policy(resp)
            return resp

    class _ListAttestors(BinauthzManagementServiceV1Beta1RestStub):
        def __hash__(self):
            return hash("ListAttestors")

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
            request: service.ListAttestorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListAttestorsResponse:
            r"""Call the list attestors method over HTTP.

            Args:
                request (~.service.ListAttestorsRequest):
                    The request object. Request message for
                [BinauthzManagementService.ListAttestors][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListAttestorsResponse:
                    Response message for
                [BinauthzManagementService.ListAttestors][].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=projects/*}/attestors",
                },
            ]
            request, metadata = self._interceptor.pre_list_attestors(request, metadata)
            pb_request = service.ListAttestorsRequest.pb(request)
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
            resp = service.ListAttestorsResponse()
            pb_resp = service.ListAttestorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_attestors(resp)
            return resp

    class _UpdateAttestor(BinauthzManagementServiceV1Beta1RestStub):
        def __hash__(self):
            return hash("UpdateAttestor")

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
            request: service.UpdateAttestorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Attestor:
            r"""Call the update attestor method over HTTP.

            Args:
                request (~.service.UpdateAttestorRequest):
                    The request object. Request message for
                [BinauthzManagementService.UpdateAttestor][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Attestor:
                    An
                [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
                that attests to container image artifacts. An existing
                attestor cannot be modified except where indicated.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1beta1/{attestor.name=projects/*/attestors/*}",
                    "body": "attestor",
                },
            ]
            request, metadata = self._interceptor.pre_update_attestor(request, metadata)
            pb_request = service.UpdateAttestorRequest.pb(request)
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
            resp = resources.Attestor()
            pb_resp = resources.Attestor.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_attestor(resp)
            return resp

    class _UpdatePolicy(BinauthzManagementServiceV1Beta1RestStub):
        def __hash__(self):
            return hash("UpdatePolicy")

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
            request: service.UpdatePolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Policy:
            r"""Call the update policy method over HTTP.

            Args:
                request (~.service.UpdatePolicyRequest):
                    The request object. Request message for
                [BinauthzManagementService.UpdatePolicy][].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Policy:
                    A
                [policy][google.cloud.binaryauthorization.v1beta1.Policy]
                for Binary Authorization.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1beta1/{policy.name=projects/*/policy}",
                    "body": "policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_policy(request, metadata)
            pb_request = service.UpdatePolicyRequest.pb(request)
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
            resp = resources.Policy()
            pb_resp = resources.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_policy(resp)
            return resp

    @property
    def create_attestor(
        self,
    ) -> Callable[[service.CreateAttestorRequest], resources.Attestor]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAttestor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_attestor(
        self,
    ) -> Callable[[service.DeleteAttestorRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAttestor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_attestor(
        self,
    ) -> Callable[[service.GetAttestorRequest], resources.Attestor]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAttestor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_policy(self) -> Callable[[service.GetPolicyRequest], resources.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_attestors(
        self,
    ) -> Callable[[service.ListAttestorsRequest], service.ListAttestorsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAttestors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_attestor(
        self,
    ) -> Callable[[service.UpdateAttestorRequest], resources.Attestor]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAttestor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_policy(
        self,
    ) -> Callable[[service.UpdatePolicyRequest], resources.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BinauthzManagementServiceV1Beta1RestTransport",)
