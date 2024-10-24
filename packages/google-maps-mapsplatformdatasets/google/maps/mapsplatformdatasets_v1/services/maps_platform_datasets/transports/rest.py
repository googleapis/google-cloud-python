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

from google.maps.mapsplatformdatasets_v1.types import dataset
from google.maps.mapsplatformdatasets_v1.types import dataset as gmm_dataset
from google.maps.mapsplatformdatasets_v1.types import maps_platform_datasets

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseMapsPlatformDatasetsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class MapsPlatformDatasetsRestInterceptor:
    """Interceptor for MapsPlatformDatasets.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MapsPlatformDatasetsRestTransport.

    .. code-block:: python
        class MyCustomMapsPlatformDatasetsInterceptor(MapsPlatformDatasetsRestInterceptor):
            def pre_create_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_fetch_dataset_errors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_dataset_errors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_datasets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_datasets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_dataset_metadata(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_dataset_metadata(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MapsPlatformDatasetsRestTransport(interceptor=MyCustomMapsPlatformDatasetsInterceptor())
        client = MapsPlatformDatasetsClient(transport=transport)


    """

    def pre_create_dataset(
        self,
        request: maps_platform_datasets.CreateDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[maps_platform_datasets.CreateDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasets server.
        """
        return request, metadata

    def post_create_dataset(self, response: gmm_dataset.Dataset) -> gmm_dataset.Dataset:
        """Post-rpc interceptor for create_dataset

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasets server but before
        it is returned to user code.
        """
        return response

    def pre_delete_dataset(
        self,
        request: maps_platform_datasets.DeleteDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[maps_platform_datasets.DeleteDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasets server.
        """
        return request, metadata

    def pre_fetch_dataset_errors(
        self,
        request: maps_platform_datasets.FetchDatasetErrorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        maps_platform_datasets.FetchDatasetErrorsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for fetch_dataset_errors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasets server.
        """
        return request, metadata

    def post_fetch_dataset_errors(
        self, response: maps_platform_datasets.FetchDatasetErrorsResponse
    ) -> maps_platform_datasets.FetchDatasetErrorsResponse:
        """Post-rpc interceptor for fetch_dataset_errors

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasets server but before
        it is returned to user code.
        """
        return response

    def pre_get_dataset(
        self,
        request: maps_platform_datasets.GetDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[maps_platform_datasets.GetDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasets server.
        """
        return request, metadata

    def post_get_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for get_dataset

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasets server but before
        it is returned to user code.
        """
        return response

    def pre_list_datasets(
        self,
        request: maps_platform_datasets.ListDatasetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[maps_platform_datasets.ListDatasetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_datasets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasets server.
        """
        return request, metadata

    def post_list_datasets(
        self, response: maps_platform_datasets.ListDatasetsResponse
    ) -> maps_platform_datasets.ListDatasetsResponse:
        """Post-rpc interceptor for list_datasets

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasets server but before
        it is returned to user code.
        """
        return response

    def pre_update_dataset_metadata(
        self,
        request: maps_platform_datasets.UpdateDatasetMetadataRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        maps_platform_datasets.UpdateDatasetMetadataRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_dataset_metadata

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasets server.
        """
        return request, metadata

    def post_update_dataset_metadata(
        self, response: gmm_dataset.Dataset
    ) -> gmm_dataset.Dataset:
        """Post-rpc interceptor for update_dataset_metadata

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasets server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MapsPlatformDatasetsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MapsPlatformDatasetsRestInterceptor


class MapsPlatformDatasetsRestTransport(_BaseMapsPlatformDatasetsRestTransport):
    """REST backend synchronous transport for MapsPlatformDatasets.

    Service definition for the Maps Platform Datasets API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "mapsplatformdatasets.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[MapsPlatformDatasetsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'mapsplatformdatasets.googleapis.com').
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
        self._interceptor = interceptor or MapsPlatformDatasetsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDataset(
        _BaseMapsPlatformDatasetsRestTransport._BaseCreateDataset,
        MapsPlatformDatasetsRestStub,
    ):
        def __hash__(self):
            return hash("MapsPlatformDatasetsRestTransport.CreateDataset")

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
            request: maps_platform_datasets.CreateDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gmm_dataset.Dataset:
            r"""Call the create dataset method over HTTP.

            Args:
                request (~.maps_platform_datasets.CreateDatasetRequest):
                    The request object. Request to create a maps dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gmm_dataset.Dataset:
                    A representation of a dataset
                resource.

            """

            http_options = (
                _BaseMapsPlatformDatasetsRestTransport._BaseCreateDataset._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_dataset(request, metadata)
            transcoded_request = _BaseMapsPlatformDatasetsRestTransport._BaseCreateDataset._get_transcoded_request(
                http_options, request
            )

            body = _BaseMapsPlatformDatasetsRestTransport._BaseCreateDataset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMapsPlatformDatasetsRestTransport._BaseCreateDataset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MapsPlatformDatasetsRestTransport._CreateDataset._get_response(
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
            resp = gmm_dataset.Dataset()
            pb_resp = gmm_dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_dataset(resp)
            return resp

    class _DeleteDataset(
        _BaseMapsPlatformDatasetsRestTransport._BaseDeleteDataset,
        MapsPlatformDatasetsRestStub,
    ):
        def __hash__(self):
            return hash("MapsPlatformDatasetsRestTransport.DeleteDataset")

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
            request: maps_platform_datasets.DeleteDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete dataset method over HTTP.

            Args:
                request (~.maps_platform_datasets.DeleteDatasetRequest):
                    The request object. Request to delete a dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseMapsPlatformDatasetsRestTransport._BaseDeleteDataset._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_dataset(request, metadata)
            transcoded_request = _BaseMapsPlatformDatasetsRestTransport._BaseDeleteDataset._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMapsPlatformDatasetsRestTransport._BaseDeleteDataset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MapsPlatformDatasetsRestTransport._DeleteDataset._get_response(
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

    class _FetchDatasetErrors(
        _BaseMapsPlatformDatasetsRestTransport._BaseFetchDatasetErrors,
        MapsPlatformDatasetsRestStub,
    ):
        def __hash__(self):
            return hash("MapsPlatformDatasetsRestTransport.FetchDatasetErrors")

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
            request: maps_platform_datasets.FetchDatasetErrorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> maps_platform_datasets.FetchDatasetErrorsResponse:
            r"""Call the fetch dataset errors method over HTTP.

            Args:
                request (~.maps_platform_datasets.FetchDatasetErrorsRequest):
                    The request object. Request to list detailed errors
                belonging to a dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.maps_platform_datasets.FetchDatasetErrorsResponse:
                    Response object of
                FetchDatasetErrors.

            """

            http_options = (
                _BaseMapsPlatformDatasetsRestTransport._BaseFetchDatasetErrors._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_dataset_errors(
                request, metadata
            )
            transcoded_request = _BaseMapsPlatformDatasetsRestTransport._BaseFetchDatasetErrors._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMapsPlatformDatasetsRestTransport._BaseFetchDatasetErrors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                MapsPlatformDatasetsRestTransport._FetchDatasetErrors._get_response(
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
            resp = maps_platform_datasets.FetchDatasetErrorsResponse()
            pb_resp = maps_platform_datasets.FetchDatasetErrorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_dataset_errors(resp)
            return resp

    class _GetDataset(
        _BaseMapsPlatformDatasetsRestTransport._BaseGetDataset,
        MapsPlatformDatasetsRestStub,
    ):
        def __hash__(self):
            return hash("MapsPlatformDatasetsRestTransport.GetDataset")

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
            request: maps_platform_datasets.GetDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataset.Dataset:
            r"""Call the get dataset method over HTTP.

            Args:
                request (~.maps_platform_datasets.GetDatasetRequest):
                    The request object. Request to get the specified dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataset.Dataset:
                    A representation of a dataset
                resource.

            """

            http_options = (
                _BaseMapsPlatformDatasetsRestTransport._BaseGetDataset._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_dataset(request, metadata)
            transcoded_request = _BaseMapsPlatformDatasetsRestTransport._BaseGetDataset._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMapsPlatformDatasetsRestTransport._BaseGetDataset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MapsPlatformDatasetsRestTransport._GetDataset._get_response(
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
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_dataset(resp)
            return resp

    class _ListDatasets(
        _BaseMapsPlatformDatasetsRestTransport._BaseListDatasets,
        MapsPlatformDatasetsRestStub,
    ):
        def __hash__(self):
            return hash("MapsPlatformDatasetsRestTransport.ListDatasets")

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
            request: maps_platform_datasets.ListDatasetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> maps_platform_datasets.ListDatasetsResponse:
            r"""Call the list datasets method over HTTP.

            Args:
                request (~.maps_platform_datasets.ListDatasetsRequest):
                    The request object. Request to list datasets for the
                project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.maps_platform_datasets.ListDatasetsResponse:
                    Response object of ListDatasets.
            """

            http_options = (
                _BaseMapsPlatformDatasetsRestTransport._BaseListDatasets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_datasets(request, metadata)
            transcoded_request = _BaseMapsPlatformDatasetsRestTransport._BaseListDatasets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMapsPlatformDatasetsRestTransport._BaseListDatasets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MapsPlatformDatasetsRestTransport._ListDatasets._get_response(
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
            resp = maps_platform_datasets.ListDatasetsResponse()
            pb_resp = maps_platform_datasets.ListDatasetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_datasets(resp)
            return resp

    class _UpdateDatasetMetadata(
        _BaseMapsPlatformDatasetsRestTransport._BaseUpdateDatasetMetadata,
        MapsPlatformDatasetsRestStub,
    ):
        def __hash__(self):
            return hash("MapsPlatformDatasetsRestTransport.UpdateDatasetMetadata")

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
            request: maps_platform_datasets.UpdateDatasetMetadataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gmm_dataset.Dataset:
            r"""Call the update dataset metadata method over HTTP.

            Args:
                request (~.maps_platform_datasets.UpdateDatasetMetadataRequest):
                    The request object. Request to update the metadata fields
                of the dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gmm_dataset.Dataset:
                    A representation of a dataset
                resource.

            """

            http_options = (
                _BaseMapsPlatformDatasetsRestTransport._BaseUpdateDatasetMetadata._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_dataset_metadata(
                request, metadata
            )
            transcoded_request = _BaseMapsPlatformDatasetsRestTransport._BaseUpdateDatasetMetadata._get_transcoded_request(
                http_options, request
            )

            body = _BaseMapsPlatformDatasetsRestTransport._BaseUpdateDatasetMetadata._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMapsPlatformDatasetsRestTransport._BaseUpdateDatasetMetadata._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                MapsPlatformDatasetsRestTransport._UpdateDatasetMetadata._get_response(
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
            resp = gmm_dataset.Dataset()
            pb_resp = gmm_dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_dataset_metadata(resp)
            return resp

    @property
    def create_dataset(
        self,
    ) -> Callable[[maps_platform_datasets.CreateDatasetRequest], gmm_dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_dataset(
        self,
    ) -> Callable[[maps_platform_datasets.DeleteDatasetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_dataset_errors(
        self,
    ) -> Callable[
        [maps_platform_datasets.FetchDatasetErrorsRequest],
        maps_platform_datasets.FetchDatasetErrorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchDatasetErrors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_dataset(
        self,
    ) -> Callable[[maps_platform_datasets.GetDatasetRequest], dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_datasets(
        self,
    ) -> Callable[
        [maps_platform_datasets.ListDatasetsRequest],
        maps_platform_datasets.ListDatasetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatasets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_dataset_metadata(
        self,
    ) -> Callable[
        [maps_platform_datasets.UpdateDatasetMetadataRequest], gmm_dataset.Dataset
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDatasetMetadata(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("MapsPlatformDatasetsRestTransport",)
