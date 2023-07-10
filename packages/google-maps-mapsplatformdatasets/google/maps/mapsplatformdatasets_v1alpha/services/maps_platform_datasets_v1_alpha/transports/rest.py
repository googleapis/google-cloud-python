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

from google.maps.mapsplatformdatasets_v1alpha.types import dataset as gmm_dataset
from google.maps.mapsplatformdatasets_v1alpha.types import maps_platform_datasets
from google.maps.mapsplatformdatasets_v1alpha.types import dataset

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import MapsPlatformDatasetsV1AlphaTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class MapsPlatformDatasetsV1AlphaRestInterceptor:
    """Interceptor for MapsPlatformDatasetsV1Alpha.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MapsPlatformDatasetsV1AlphaRestTransport.

    .. code-block:: python
        class MyCustomMapsPlatformDatasetsV1AlphaInterceptor(MapsPlatformDatasetsV1AlphaRestInterceptor):
            def pre_create_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_dataset_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

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

            def pre_list_dataset_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_dataset_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_dataset_metadata(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_dataset_metadata(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MapsPlatformDatasetsV1AlphaRestTransport(interceptor=MyCustomMapsPlatformDatasetsV1AlphaInterceptor())
        client = MapsPlatformDatasetsV1AlphaClient(transport=transport)


    """

    def pre_create_dataset(
        self,
        request: maps_platform_datasets.CreateDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[maps_platform_datasets.CreateDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasetsV1Alpha server.
        """
        return request, metadata

    def post_create_dataset(self, response: gmm_dataset.Dataset) -> gmm_dataset.Dataset:
        """Post-rpc interceptor for create_dataset

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasetsV1Alpha server but before
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
        before they are sent to the MapsPlatformDatasetsV1Alpha server.
        """
        return request, metadata

    def pre_delete_dataset_version(
        self,
        request: maps_platform_datasets.DeleteDatasetVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        maps_platform_datasets.DeleteDatasetVersionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_dataset_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasetsV1Alpha server.
        """
        return request, metadata

    def pre_get_dataset(
        self,
        request: maps_platform_datasets.GetDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[maps_platform_datasets.GetDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasetsV1Alpha server.
        """
        return request, metadata

    def post_get_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for get_dataset

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasetsV1Alpha server but before
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
        before they are sent to the MapsPlatformDatasetsV1Alpha server.
        """
        return request, metadata

    def post_list_datasets(
        self, response: maps_platform_datasets.ListDatasetsResponse
    ) -> maps_platform_datasets.ListDatasetsResponse:
        """Post-rpc interceptor for list_datasets

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasetsV1Alpha server but before
        it is returned to user code.
        """
        return response

    def pre_list_dataset_versions(
        self,
        request: maps_platform_datasets.ListDatasetVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        maps_platform_datasets.ListDatasetVersionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_dataset_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MapsPlatformDatasetsV1Alpha server.
        """
        return request, metadata

    def post_list_dataset_versions(
        self, response: maps_platform_datasets.ListDatasetVersionsResponse
    ) -> maps_platform_datasets.ListDatasetVersionsResponse:
        """Post-rpc interceptor for list_dataset_versions

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasetsV1Alpha server but before
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
        before they are sent to the MapsPlatformDatasetsV1Alpha server.
        """
        return request, metadata

    def post_update_dataset_metadata(
        self, response: gmm_dataset.Dataset
    ) -> gmm_dataset.Dataset:
        """Post-rpc interceptor for update_dataset_metadata

        Override in a subclass to manipulate the response
        after it is returned by the MapsPlatformDatasetsV1Alpha server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MapsPlatformDatasetsV1AlphaRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MapsPlatformDatasetsV1AlphaRestInterceptor


class MapsPlatformDatasetsV1AlphaRestTransport(MapsPlatformDatasetsV1AlphaTransport):
    """REST backend transport for MapsPlatformDatasetsV1Alpha.

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
        interceptor: Optional[MapsPlatformDatasetsV1AlphaRestInterceptor] = None,
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
        self._interceptor = interceptor or MapsPlatformDatasetsV1AlphaRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDataset(MapsPlatformDatasetsV1AlphaRestStub):
        def __hash__(self):
            return hash("CreateDataset")

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
                    A representation of a maps platform
                dataset.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*}/datasets",
                    "body": "dataset",
                },
            ]
            request, metadata = self._interceptor.pre_create_dataset(request, metadata)
            pb_request = maps_platform_datasets.CreateDatasetRequest.pb(request)
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
            resp = gmm_dataset.Dataset()
            pb_resp = gmm_dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_dataset(resp)
            return resp

    class _DeleteDataset(MapsPlatformDatasetsV1AlphaRestStub):
        def __hash__(self):
            return hash("DeleteDataset")

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
                The dataset to be deleted.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=projects/*/datasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_dataset(request, metadata)
            pb_request = maps_platform_datasets.DeleteDatasetRequest.pb(request)
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

    class _DeleteDatasetVersion(MapsPlatformDatasetsV1AlphaRestStub):
        def __hash__(self):
            return hash("DeleteDatasetVersion")

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
            request: maps_platform_datasets.DeleteDatasetVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete dataset version method over HTTP.

            Args:
                request (~.maps_platform_datasets.DeleteDatasetVersionRequest):
                    The request object. Request to delete a version of a
                dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=projects/*/datasets/*}:deleteVersion",
                },
            ]
            request, metadata = self._interceptor.pre_delete_dataset_version(
                request, metadata
            )
            pb_request = maps_platform_datasets.DeleteDatasetVersionRequest.pb(request)
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

    class _GetDataset(MapsPlatformDatasetsV1AlphaRestStub):
        def __hash__(self):
            return hash("GetDataset")

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
                    A representation of a maps platform
                dataset.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/datasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_dataset(request, metadata)
            pb_request = maps_platform_datasets.GetDatasetRequest.pb(request)
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
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_dataset(resp)
            return resp

    class _ListDatasets(MapsPlatformDatasetsV1AlphaRestStub):
        def __hash__(self):
            return hash("ListDatasets")

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
                    Response to list datasets for the
                project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*}/datasets",
                },
            ]
            request, metadata = self._interceptor.pre_list_datasets(request, metadata)
            pb_request = maps_platform_datasets.ListDatasetsRequest.pb(request)
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
            resp = maps_platform_datasets.ListDatasetsResponse()
            pb_resp = maps_platform_datasets.ListDatasetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_datasets(resp)
            return resp

    class _ListDatasetVersions(MapsPlatformDatasetsV1AlphaRestStub):
        def __hash__(self):
            return hash("ListDatasetVersions")

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
            request: maps_platform_datasets.ListDatasetVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> maps_platform_datasets.ListDatasetVersionsResponse:
            r"""Call the list dataset versions method over HTTP.

            Args:
                request (~.maps_platform_datasets.ListDatasetVersionsRequest):
                    The request object. Request to list of all versions of
                the dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.maps_platform_datasets.ListDatasetVersionsResponse:
                    Response with list of all versions of
                the dataset.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/datasets/*}:listVersions",
                },
            ]
            request, metadata = self._interceptor.pre_list_dataset_versions(
                request, metadata
            )
            pb_request = maps_platform_datasets.ListDatasetVersionsRequest.pb(request)
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
            resp = maps_platform_datasets.ListDatasetVersionsResponse()
            pb_resp = maps_platform_datasets.ListDatasetVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_dataset_versions(resp)
            return resp

    class _UpdateDatasetMetadata(MapsPlatformDatasetsV1AlphaRestStub):
        def __hash__(self):
            return hash("UpdateDatasetMetadata")

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
                    A representation of a maps platform
                dataset.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{dataset.name=projects/*/datasets/*}",
                    "body": "dataset",
                },
            ]
            request, metadata = self._interceptor.pre_update_dataset_metadata(
                request, metadata
            )
            pb_request = maps_platform_datasets.UpdateDatasetMetadataRequest.pb(request)
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
    def delete_dataset_version(
        self,
    ) -> Callable[
        [maps_platform_datasets.DeleteDatasetVersionRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDatasetVersion(self._session, self._host, self._interceptor)  # type: ignore

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
    def list_dataset_versions(
        self,
    ) -> Callable[
        [maps_platform_datasets.ListDatasetVersionsRequest],
        maps_platform_datasets.ListDatasetVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatasetVersions(self._session, self._host, self._interceptor)  # type: ignore

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


__all__ = ("MapsPlatformDatasetsV1AlphaRestTransport",)
