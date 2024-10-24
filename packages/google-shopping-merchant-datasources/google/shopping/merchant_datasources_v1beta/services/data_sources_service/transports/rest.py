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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.shopping.merchant_datasources_v1beta.types import datasources

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDataSourcesServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DataSourcesServiceRestInterceptor:
    """Interceptor for DataSourcesService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DataSourcesServiceRestTransport.

    .. code-block:: python
        class MyCustomDataSourcesServiceInterceptor(DataSourcesServiceRestInterceptor):
            def pre_create_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_data_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_fetch_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_data_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_source(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DataSourcesServiceRestTransport(interceptor=MyCustomDataSourcesServiceInterceptor())
        client = DataSourcesServiceClient(transport=transport)


    """

    def pre_create_data_source(
        self,
        request: datasources.CreateDataSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datasources.CreateDataSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataSourcesService server.
        """
        return request, metadata

    def post_create_data_source(
        self, response: datasources.DataSource
    ) -> datasources.DataSource:
        """Post-rpc interceptor for create_data_source

        Override in a subclass to manipulate the response
        after it is returned by the DataSourcesService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_data_source(
        self,
        request: datasources.DeleteDataSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datasources.DeleteDataSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataSourcesService server.
        """
        return request, metadata

    def pre_fetch_data_source(
        self,
        request: datasources.FetchDataSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datasources.FetchDataSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataSourcesService server.
        """
        return request, metadata

    def pre_get_data_source(
        self,
        request: datasources.GetDataSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datasources.GetDataSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataSourcesService server.
        """
        return request, metadata

    def post_get_data_source(
        self, response: datasources.DataSource
    ) -> datasources.DataSource:
        """Post-rpc interceptor for get_data_source

        Override in a subclass to manipulate the response
        after it is returned by the DataSourcesService server but before
        it is returned to user code.
        """
        return response

    def pre_list_data_sources(
        self,
        request: datasources.ListDataSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datasources.ListDataSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_data_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataSourcesService server.
        """
        return request, metadata

    def post_list_data_sources(
        self, response: datasources.ListDataSourcesResponse
    ) -> datasources.ListDataSourcesResponse:
        """Post-rpc interceptor for list_data_sources

        Override in a subclass to manipulate the response
        after it is returned by the DataSourcesService server but before
        it is returned to user code.
        """
        return response

    def pre_update_data_source(
        self,
        request: datasources.UpdateDataSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datasources.UpdateDataSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_data_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataSourcesService server.
        """
        return request, metadata

    def post_update_data_source(
        self, response: datasources.DataSource
    ) -> datasources.DataSource:
        """Post-rpc interceptor for update_data_source

        Override in a subclass to manipulate the response
        after it is returned by the DataSourcesService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DataSourcesServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataSourcesServiceRestInterceptor


class DataSourcesServiceRestTransport(_BaseDataSourcesServiceRestTransport):
    """REST backend synchronous transport for DataSourcesService.

    Service to manage primary, supplemental, inventory and other data
    sources. See more in the `Merchant
    Center <https://support.google.com/merchants/answer/7439058>`__ help
    article.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "merchantapi.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DataSourcesServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'merchantapi.googleapis.com').
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
        self._interceptor = interceptor or DataSourcesServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDataSource(
        _BaseDataSourcesServiceRestTransport._BaseCreateDataSource,
        DataSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataSourcesServiceRestTransport.CreateDataSource")

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
            request: datasources.CreateDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datasources.DataSource:
            r"""Call the create data source method over HTTP.

            Args:
                request (~.datasources.CreateDataSourceRequest):
                    The request object. Request message for the
                CreateDataSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datasources.DataSource:
                    The `data
                source <https://support.google.com/merchants/answer/7439058>`__
                for the Merchant Center account.

            """

            http_options = (
                _BaseDataSourcesServiceRestTransport._BaseCreateDataSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_data_source(
                request, metadata
            )
            transcoded_request = _BaseDataSourcesServiceRestTransport._BaseCreateDataSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataSourcesServiceRestTransport._BaseCreateDataSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataSourcesServiceRestTransport._BaseCreateDataSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataSourcesServiceRestTransport._CreateDataSource._get_response(
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
            resp = datasources.DataSource()
            pb_resp = datasources.DataSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_data_source(resp)
            return resp

    class _DeleteDataSource(
        _BaseDataSourcesServiceRestTransport._BaseDeleteDataSource,
        DataSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataSourcesServiceRestTransport.DeleteDataSource")

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
            request: datasources.DeleteDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete data source method over HTTP.

            Args:
                request (~.datasources.DeleteDataSourceRequest):
                    The request object. Request message for the
                DeleteDataSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseDataSourcesServiceRestTransport._BaseDeleteDataSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_data_source(
                request, metadata
            )
            transcoded_request = _BaseDataSourcesServiceRestTransport._BaseDeleteDataSource._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataSourcesServiceRestTransport._BaseDeleteDataSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataSourcesServiceRestTransport._DeleteDataSource._get_response(
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

    class _FetchDataSource(
        _BaseDataSourcesServiceRestTransport._BaseFetchDataSource,
        DataSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataSourcesServiceRestTransport.FetchDataSource")

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
            request: datasources.FetchDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the fetch data source method over HTTP.

            Args:
                request (~.datasources.FetchDataSourceRequest):
                    The request object. Request message for the
                FetchDataSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseDataSourcesServiceRestTransport._BaseFetchDataSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_data_source(
                request, metadata
            )
            transcoded_request = _BaseDataSourcesServiceRestTransport._BaseFetchDataSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataSourcesServiceRestTransport._BaseFetchDataSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataSourcesServiceRestTransport._BaseFetchDataSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataSourcesServiceRestTransport._FetchDataSource._get_response(
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

    class _GetDataSource(
        _BaseDataSourcesServiceRestTransport._BaseGetDataSource,
        DataSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataSourcesServiceRestTransport.GetDataSource")

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
            request: datasources.GetDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datasources.DataSource:
            r"""Call the get data source method over HTTP.

            Args:
                request (~.datasources.GetDataSourceRequest):
                    The request object. Request message for the GetDataSource
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datasources.DataSource:
                    The `data
                source <https://support.google.com/merchants/answer/7439058>`__
                for the Merchant Center account.

            """

            http_options = (
                _BaseDataSourcesServiceRestTransport._BaseGetDataSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_data_source(request, metadata)
            transcoded_request = _BaseDataSourcesServiceRestTransport._BaseGetDataSource._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataSourcesServiceRestTransport._BaseGetDataSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataSourcesServiceRestTransport._GetDataSource._get_response(
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
            resp = datasources.DataSource()
            pb_resp = datasources.DataSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_source(resp)
            return resp

    class _ListDataSources(
        _BaseDataSourcesServiceRestTransport._BaseListDataSources,
        DataSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataSourcesServiceRestTransport.ListDataSources")

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
            request: datasources.ListDataSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datasources.ListDataSourcesResponse:
            r"""Call the list data sources method over HTTP.

            Args:
                request (~.datasources.ListDataSourcesRequest):
                    The request object. Request message for the
                ListDataSources method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datasources.ListDataSourcesResponse:
                    Response message for the
                ListDataSources method.

            """

            http_options = (
                _BaseDataSourcesServiceRestTransport._BaseListDataSources._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_data_sources(
                request, metadata
            )
            transcoded_request = _BaseDataSourcesServiceRestTransport._BaseListDataSources._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataSourcesServiceRestTransport._BaseListDataSources._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataSourcesServiceRestTransport._ListDataSources._get_response(
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
            resp = datasources.ListDataSourcesResponse()
            pb_resp = datasources.ListDataSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_data_sources(resp)
            return resp

    class _UpdateDataSource(
        _BaseDataSourcesServiceRestTransport._BaseUpdateDataSource,
        DataSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("DataSourcesServiceRestTransport.UpdateDataSource")

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
            request: datasources.UpdateDataSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datasources.DataSource:
            r"""Call the update data source method over HTTP.

            Args:
                request (~.datasources.UpdateDataSourceRequest):
                    The request object. Request message for the
                UpdateDataSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datasources.DataSource:
                    The `data
                source <https://support.google.com/merchants/answer/7439058>`__
                for the Merchant Center account.

            """

            http_options = (
                _BaseDataSourcesServiceRestTransport._BaseUpdateDataSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_data_source(
                request, metadata
            )
            transcoded_request = _BaseDataSourcesServiceRestTransport._BaseUpdateDataSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataSourcesServiceRestTransport._BaseUpdateDataSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataSourcesServiceRestTransport._BaseUpdateDataSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataSourcesServiceRestTransport._UpdateDataSource._get_response(
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
            resp = datasources.DataSource()
            pb_resp = datasources.DataSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_data_source(resp)
            return resp

    @property
    def create_data_source(
        self,
    ) -> Callable[[datasources.CreateDataSourceRequest], datasources.DataSource]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_data_source(
        self,
    ) -> Callable[[datasources.DeleteDataSourceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_data_source(
        self,
    ) -> Callable[[datasources.FetchDataSourceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_source(
        self,
    ) -> Callable[[datasources.GetDataSourceRequest], datasources.DataSource]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_data_sources(
        self,
    ) -> Callable[
        [datasources.ListDataSourcesRequest], datasources.ListDataSourcesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDataSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_data_source(
        self,
    ) -> Callable[[datasources.UpdateDataSourceRequest], datasources.DataSource]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DataSourcesServiceRestTransport",)
