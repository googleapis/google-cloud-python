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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflow_v2beta1.types import sip_trunk
from google.cloud.dialogflow_v2beta1.types import sip_trunk as gcd_sip_trunk

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSipTrunksRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SipTrunksRestInterceptor:
    """Interceptor for SipTrunks.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SipTrunksRestTransport.

    .. code-block:: python
        class MyCustomSipTrunksInterceptor(SipTrunksRestInterceptor):
            def pre_create_sip_trunk(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_sip_trunk(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_sip_trunk(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_sip_trunk(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_sip_trunk(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sip_trunks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sip_trunks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_sip_trunk(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_sip_trunk(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SipTrunksRestTransport(interceptor=MyCustomSipTrunksInterceptor())
        client = SipTrunksClient(transport=transport)


    """

    def pre_create_sip_trunk(
        self,
        request: gcd_sip_trunk.CreateSipTrunkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_sip_trunk.CreateSipTrunkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_sip_trunk

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_create_sip_trunk(
        self, response: gcd_sip_trunk.SipTrunk
    ) -> gcd_sip_trunk.SipTrunk:
        """Post-rpc interceptor for create_sip_trunk

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response

    def pre_delete_sip_trunk(
        self,
        request: sip_trunk.DeleteSipTrunkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[sip_trunk.DeleteSipTrunkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_sip_trunk

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def pre_get_sip_trunk(
        self, request: sip_trunk.GetSipTrunkRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[sip_trunk.GetSipTrunkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_sip_trunk

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_get_sip_trunk(self, response: sip_trunk.SipTrunk) -> sip_trunk.SipTrunk:
        """Post-rpc interceptor for get_sip_trunk

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response

    def pre_list_sip_trunks(
        self,
        request: sip_trunk.ListSipTrunksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[sip_trunk.ListSipTrunksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sip_trunks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_list_sip_trunks(
        self, response: sip_trunk.ListSipTrunksResponse
    ) -> sip_trunk.ListSipTrunksResponse:
        """Post-rpc interceptor for list_sip_trunks

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response

    def pre_update_sip_trunk(
        self,
        request: gcd_sip_trunk.UpdateSipTrunkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_sip_trunk.UpdateSipTrunkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_sip_trunk

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_update_sip_trunk(
        self, response: gcd_sip_trunk.SipTrunk
    ) -> gcd_sip_trunk.SipTrunk:
        """Post-rpc interceptor for update_sip_trunk

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
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
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SipTrunks server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the SipTrunks server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SipTrunksRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SipTrunksRestInterceptor


class SipTrunksRestTransport(_BaseSipTrunksRestTransport):
    """REST backend synchronous transport for SipTrunks.

    Service for managing
    [SipTrunks][google.cloud.dialogflow.v2beta1.SipTrunk].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SipTrunksRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
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
        self._interceptor = interceptor or SipTrunksRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateSipTrunk(
        _BaseSipTrunksRestTransport._BaseCreateSipTrunk, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.CreateSipTrunk")

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
            request: gcd_sip_trunk.CreateSipTrunkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_sip_trunk.SipTrunk:
            r"""Call the create sip trunk method over HTTP.

            Args:
                request (~.gcd_sip_trunk.CreateSipTrunkRequest):
                    The request object. The request message for
                [SipTrunks.CreateSipTrunk][google.cloud.dialogflow.v2beta1.SipTrunks.CreateSipTrunk].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_sip_trunk.SipTrunk:
                    SipTrunk is the resource that
                represents a SIP trunk to connect to
                Google Telephony platform SIP trunking
                service.

            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseCreateSipTrunk._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_sip_trunk(
                request, metadata
            )
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseCreateSipTrunk._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseSipTrunksRestTransport._BaseCreateSipTrunk._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseCreateSipTrunk._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._CreateSipTrunk._get_response(
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
            resp = gcd_sip_trunk.SipTrunk()
            pb_resp = gcd_sip_trunk.SipTrunk.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_sip_trunk(resp)
            return resp

    class _DeleteSipTrunk(
        _BaseSipTrunksRestTransport._BaseDeleteSipTrunk, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.DeleteSipTrunk")

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
            request: sip_trunk.DeleteSipTrunkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete sip trunk method over HTTP.

            Args:
                request (~.sip_trunk.DeleteSipTrunkRequest):
                    The request object. The request message for
                [SipTrunks.DeleteSipTrunk][google.cloud.dialogflow.v2beta1.SipTrunks.DeleteSipTrunk].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseDeleteSipTrunk._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_sip_trunk(
                request, metadata
            )
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseDeleteSipTrunk._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseDeleteSipTrunk._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._DeleteSipTrunk._get_response(
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

    class _GetSipTrunk(_BaseSipTrunksRestTransport._BaseGetSipTrunk, SipTrunksRestStub):
        def __hash__(self):
            return hash("SipTrunksRestTransport.GetSipTrunk")

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
            request: sip_trunk.GetSipTrunkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sip_trunk.SipTrunk:
            r"""Call the get sip trunk method over HTTP.

            Args:
                request (~.sip_trunk.GetSipTrunkRequest):
                    The request object. The request message for
                [SipTrunks.GetSipTrunk][google.cloud.dialogflow.v2beta1.SipTrunks.GetSipTrunk].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sip_trunk.SipTrunk:
                    SipTrunk is the resource that
                represents a SIP trunk to connect to
                Google Telephony platform SIP trunking
                service.

            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseGetSipTrunk._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_sip_trunk(request, metadata)
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseGetSipTrunk._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseGetSipTrunk._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._GetSipTrunk._get_response(
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
            resp = sip_trunk.SipTrunk()
            pb_resp = sip_trunk.SipTrunk.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_sip_trunk(resp)
            return resp

    class _ListSipTrunks(
        _BaseSipTrunksRestTransport._BaseListSipTrunks, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.ListSipTrunks")

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
            request: sip_trunk.ListSipTrunksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sip_trunk.ListSipTrunksResponse:
            r"""Call the list sip trunks method over HTTP.

            Args:
                request (~.sip_trunk.ListSipTrunksRequest):
                    The request object. The request message for
                [SipTrunks.ListSipTrunks][google.cloud.dialogflow.v2beta1.SipTrunks.ListSipTrunks].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sip_trunk.ListSipTrunksResponse:
                    The response message for
                [SipTrunks.ListSipTrunks][google.cloud.dialogflow.v2beta1.SipTrunks.ListSipTrunks].

            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseListSipTrunks._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_sip_trunks(request, metadata)
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseListSipTrunks._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseListSipTrunks._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._ListSipTrunks._get_response(
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
            resp = sip_trunk.ListSipTrunksResponse()
            pb_resp = sip_trunk.ListSipTrunksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sip_trunks(resp)
            return resp

    class _UpdateSipTrunk(
        _BaseSipTrunksRestTransport._BaseUpdateSipTrunk, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.UpdateSipTrunk")

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
            request: gcd_sip_trunk.UpdateSipTrunkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_sip_trunk.SipTrunk:
            r"""Call the update sip trunk method over HTTP.

            Args:
                request (~.gcd_sip_trunk.UpdateSipTrunkRequest):
                    The request object. The request message for
                [SipTrunks.UpdateSipTrunk][google.cloud.dialogflow.v2beta1.SipTrunks.UpdateSipTrunk].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_sip_trunk.SipTrunk:
                    SipTrunk is the resource that
                represents a SIP trunk to connect to
                Google Telephony platform SIP trunking
                service.

            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseUpdateSipTrunk._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_sip_trunk(
                request, metadata
            )
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseUpdateSipTrunk._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseSipTrunksRestTransport._BaseUpdateSipTrunk._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseUpdateSipTrunk._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._UpdateSipTrunk._get_response(
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
            resp = gcd_sip_trunk.SipTrunk()
            pb_resp = gcd_sip_trunk.SipTrunk.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_sip_trunk(resp)
            return resp

    @property
    def create_sip_trunk(
        self,
    ) -> Callable[[gcd_sip_trunk.CreateSipTrunkRequest], gcd_sip_trunk.SipTrunk]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSipTrunk(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_sip_trunk(
        self,
    ) -> Callable[[sip_trunk.DeleteSipTrunkRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSipTrunk(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_sip_trunk(
        self,
    ) -> Callable[[sip_trunk.GetSipTrunkRequest], sip_trunk.SipTrunk]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSipTrunk(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sip_trunks(
        self,
    ) -> Callable[[sip_trunk.ListSipTrunksRequest], sip_trunk.ListSipTrunksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSipTrunks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_sip_trunk(
        self,
    ) -> Callable[[gcd_sip_trunk.UpdateSipTrunkRequest], gcd_sip_trunk.SipTrunk]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSipTrunk(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseSipTrunksRestTransport._BaseGetLocation, SipTrunksRestStub):
        def __hash__(self):
            return hash("SipTrunksRestTransport.GetLocation")

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
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._GetLocation._get_response(
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
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseSipTrunksRestTransport._BaseListLocations, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.ListLocations")

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
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._ListLocations._get_response(
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
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseSipTrunksRestTransport._BaseCancelOperation, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseSipTrunksRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseSipTrunksRestTransport._BaseGetOperation, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.GetOperation")

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
                _BaseSipTrunksRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._GetOperation._get_response(
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
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseSipTrunksRestTransport._BaseListOperations, SipTrunksRestStub
    ):
        def __hash__(self):
            return hash("SipTrunksRestTransport.ListOperations")

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
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseSipTrunksRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseSipTrunksRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseSipTrunksRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = SipTrunksRestTransport._ListOperations._get_response(
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
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SipTrunksRestTransport",)
