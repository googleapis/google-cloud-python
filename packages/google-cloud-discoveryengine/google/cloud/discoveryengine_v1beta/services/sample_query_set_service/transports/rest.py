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

from google.cloud.discoveryengine_v1beta.types import (
    sample_query_set as gcd_sample_query_set,
)
from google.cloud.discoveryengine_v1beta.types import sample_query_set
from google.cloud.discoveryengine_v1beta.types import sample_query_set_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSampleQuerySetServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class SampleQuerySetServiceRestInterceptor:
    """Interceptor for SampleQuerySetService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SampleQuerySetServiceRestTransport.

    .. code-block:: python
        class MyCustomSampleQuerySetServiceInterceptor(SampleQuerySetServiceRestInterceptor):
            def pre_create_sample_query_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_sample_query_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_sample_query_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_sample_query_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_sample_query_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sample_query_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sample_query_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_sample_query_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_sample_query_set(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SampleQuerySetServiceRestTransport(interceptor=MyCustomSampleQuerySetServiceInterceptor())
        client = SampleQuerySetServiceClient(transport=transport)


    """

    def pre_create_sample_query_set(
        self,
        request: sample_query_set_service.CreateSampleQuerySetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        sample_query_set_service.CreateSampleQuerySetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_sample_query_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def post_create_sample_query_set(
        self, response: gcd_sample_query_set.SampleQuerySet
    ) -> gcd_sample_query_set.SampleQuerySet:
        """Post-rpc interceptor for create_sample_query_set

        Override in a subclass to manipulate the response
        after it is returned by the SampleQuerySetService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_sample_query_set(
        self,
        request: sample_query_set_service.DeleteSampleQuerySetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        sample_query_set_service.DeleteSampleQuerySetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_sample_query_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def pre_get_sample_query_set(
        self,
        request: sample_query_set_service.GetSampleQuerySetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        sample_query_set_service.GetSampleQuerySetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_sample_query_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def post_get_sample_query_set(
        self, response: sample_query_set.SampleQuerySet
    ) -> sample_query_set.SampleQuerySet:
        """Post-rpc interceptor for get_sample_query_set

        Override in a subclass to manipulate the response
        after it is returned by the SampleQuerySetService server but before
        it is returned to user code.
        """
        return response

    def pre_list_sample_query_sets(
        self,
        request: sample_query_set_service.ListSampleQuerySetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        sample_query_set_service.ListSampleQuerySetsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_sample_query_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def post_list_sample_query_sets(
        self, response: sample_query_set_service.ListSampleQuerySetsResponse
    ) -> sample_query_set_service.ListSampleQuerySetsResponse:
        """Post-rpc interceptor for list_sample_query_sets

        Override in a subclass to manipulate the response
        after it is returned by the SampleQuerySetService server but before
        it is returned to user code.
        """
        return response

    def pre_update_sample_query_set(
        self,
        request: sample_query_set_service.UpdateSampleQuerySetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        sample_query_set_service.UpdateSampleQuerySetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_sample_query_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def post_update_sample_query_set(
        self, response: gcd_sample_query_set.SampleQuerySet
    ) -> gcd_sample_query_set.SampleQuerySet:
        """Post-rpc interceptor for update_sample_query_set

        Override in a subclass to manipulate the response
        after it is returned by the SampleQuerySetService server but before
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
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the SampleQuerySetService server but before
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
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the SampleQuerySetService server but before
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
        before they are sent to the SampleQuerySetService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the SampleQuerySetService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SampleQuerySetServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SampleQuerySetServiceRestInterceptor


class SampleQuerySetServiceRestTransport(_BaseSampleQuerySetServiceRestTransport):
    """REST backend synchronous transport for SampleQuerySetService.

    Service for managing
    [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]s,

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "discoveryengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SampleQuerySetServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'discoveryengine.googleapis.com').
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
        self._interceptor = interceptor or SampleQuerySetServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateSampleQuerySet(
        _BaseSampleQuerySetServiceRestTransport._BaseCreateSampleQuerySet,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.CreateSampleQuerySet")

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
            request: sample_query_set_service.CreateSampleQuerySetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_sample_query_set.SampleQuerySet:
            r"""Call the create sample query set method over HTTP.

            Args:
                request (~.sample_query_set_service.CreateSampleQuerySetRequest):
                    The request object. Request message for
                [SampleQuerySetService.CreateSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.CreateSampleQuerySet]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_sample_query_set.SampleQuerySet:
                    A SampleQuerySet is the parent
                resource of SampleQuery, and contains
                the configurations shared by all
                SampleQuery under it.

            """

            http_options = (
                _BaseSampleQuerySetServiceRestTransport._BaseCreateSampleQuerySet._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_sample_query_set(
                request, metadata
            )
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseCreateSampleQuerySet._get_transcoded_request(
                http_options, request
            )

            body = _BaseSampleQuerySetServiceRestTransport._BaseCreateSampleQuerySet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseCreateSampleQuerySet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SampleQuerySetServiceRestTransport._CreateSampleQuerySet._get_response(
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
            resp = gcd_sample_query_set.SampleQuerySet()
            pb_resp = gcd_sample_query_set.SampleQuerySet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_sample_query_set(resp)
            return resp

    class _DeleteSampleQuerySet(
        _BaseSampleQuerySetServiceRestTransport._BaseDeleteSampleQuerySet,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.DeleteSampleQuerySet")

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
            request: sample_query_set_service.DeleteSampleQuerySetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete sample query set method over HTTP.

            Args:
                request (~.sample_query_set_service.DeleteSampleQuerySetRequest):
                    The request object. Request message for
                [SampleQuerySetService.DeleteSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.DeleteSampleQuerySet]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseSampleQuerySetServiceRestTransport._BaseDeleteSampleQuerySet._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_sample_query_set(
                request, metadata
            )
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseDeleteSampleQuerySet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseDeleteSampleQuerySet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SampleQuerySetServiceRestTransport._DeleteSampleQuerySet._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetSampleQuerySet(
        _BaseSampleQuerySetServiceRestTransport._BaseGetSampleQuerySet,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.GetSampleQuerySet")

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
            request: sample_query_set_service.GetSampleQuerySetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sample_query_set.SampleQuerySet:
            r"""Call the get sample query set method over HTTP.

            Args:
                request (~.sample_query_set_service.GetSampleQuerySetRequest):
                    The request object. Request message for
                [SampleQuerySetService.GetSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.GetSampleQuerySet]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sample_query_set.SampleQuerySet:
                    A SampleQuerySet is the parent
                resource of SampleQuery, and contains
                the configurations shared by all
                SampleQuery under it.

            """

            http_options = (
                _BaseSampleQuerySetServiceRestTransport._BaseGetSampleQuerySet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_sample_query_set(
                request, metadata
            )
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseGetSampleQuerySet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseGetSampleQuerySet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SampleQuerySetServiceRestTransport._GetSampleQuerySet._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = sample_query_set.SampleQuerySet()
            pb_resp = sample_query_set.SampleQuerySet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_sample_query_set(resp)
            return resp

    class _ListSampleQuerySets(
        _BaseSampleQuerySetServiceRestTransport._BaseListSampleQuerySets,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.ListSampleQuerySets")

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
            request: sample_query_set_service.ListSampleQuerySetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> sample_query_set_service.ListSampleQuerySetsResponse:
            r"""Call the list sample query sets method over HTTP.

            Args:
                request (~.sample_query_set_service.ListSampleQuerySetsRequest):
                    The request object. Request message for
                [SampleQuerySetService.ListSampleQuerySets][google.cloud.discoveryengine.v1beta.SampleQuerySetService.ListSampleQuerySets]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.sample_query_set_service.ListSampleQuerySetsResponse:
                    Response message for
                [SampleQuerySetService.ListSampleQuerySets][google.cloud.discoveryengine.v1beta.SampleQuerySetService.ListSampleQuerySets]
                method.

            """

            http_options = (
                _BaseSampleQuerySetServiceRestTransport._BaseListSampleQuerySets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_sample_query_sets(
                request, metadata
            )
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseListSampleQuerySets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseListSampleQuerySets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SampleQuerySetServiceRestTransport._ListSampleQuerySets._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = sample_query_set_service.ListSampleQuerySetsResponse()
            pb_resp = sample_query_set_service.ListSampleQuerySetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sample_query_sets(resp)
            return resp

    class _UpdateSampleQuerySet(
        _BaseSampleQuerySetServiceRestTransport._BaseUpdateSampleQuerySet,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.UpdateSampleQuerySet")

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
            request: sample_query_set_service.UpdateSampleQuerySetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_sample_query_set.SampleQuerySet:
            r"""Call the update sample query set method over HTTP.

            Args:
                request (~.sample_query_set_service.UpdateSampleQuerySetRequest):
                    The request object. Request message for
                [SampleQuerySetService.UpdateSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.UpdateSampleQuerySet]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_sample_query_set.SampleQuerySet:
                    A SampleQuerySet is the parent
                resource of SampleQuery, and contains
                the configurations shared by all
                SampleQuery under it.

            """

            http_options = (
                _BaseSampleQuerySetServiceRestTransport._BaseUpdateSampleQuerySet._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_sample_query_set(
                request, metadata
            )
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseUpdateSampleQuerySet._get_transcoded_request(
                http_options, request
            )

            body = _BaseSampleQuerySetServiceRestTransport._BaseUpdateSampleQuerySet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseUpdateSampleQuerySet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SampleQuerySetServiceRestTransport._UpdateSampleQuerySet._get_response(
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
            resp = gcd_sample_query_set.SampleQuerySet()
            pb_resp = gcd_sample_query_set.SampleQuerySet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_sample_query_set(resp)
            return resp

    @property
    def create_sample_query_set(
        self,
    ) -> Callable[
        [sample_query_set_service.CreateSampleQuerySetRequest],
        gcd_sample_query_set.SampleQuerySet,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSampleQuerySet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_sample_query_set(
        self,
    ) -> Callable[
        [sample_query_set_service.DeleteSampleQuerySetRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSampleQuerySet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_sample_query_set(
        self,
    ) -> Callable[
        [sample_query_set_service.GetSampleQuerySetRequest],
        sample_query_set.SampleQuerySet,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSampleQuerySet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sample_query_sets(
        self,
    ) -> Callable[
        [sample_query_set_service.ListSampleQuerySetsRequest],
        sample_query_set_service.ListSampleQuerySetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSampleQuerySets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_sample_query_set(
        self,
    ) -> Callable[
        [sample_query_set_service.UpdateSampleQuerySetRequest],
        gcd_sample_query_set.SampleQuerySet,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSampleQuerySet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseSampleQuerySetServiceRestTransport._BaseCancelOperation,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.CancelOperation")

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
                _BaseSampleQuerySetServiceRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseSampleQuerySetServiceRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SampleQuerySetServiceRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseSampleQuerySetServiceRestTransport._BaseGetOperation,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.GetOperation")

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
                _BaseSampleQuerySetServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SampleQuerySetServiceRestTransport._GetOperation._get_response(
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
        _BaseSampleQuerySetServiceRestTransport._BaseListOperations,
        SampleQuerySetServiceRestStub,
    ):
        def __hash__(self):
            return hash("SampleQuerySetServiceRestTransport.ListOperations")

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
                _BaseSampleQuerySetServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseSampleQuerySetServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSampleQuerySetServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SampleQuerySetServiceRestTransport._ListOperations._get_response(
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


__all__ = ("SampleQuerySetServiceRestTransport",)
