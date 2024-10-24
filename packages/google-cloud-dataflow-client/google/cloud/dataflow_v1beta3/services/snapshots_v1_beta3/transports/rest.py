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
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dataflow_v1beta3.types import snapshots

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSnapshotsV1Beta3RestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SnapshotsV1Beta3RestInterceptor:
    """Interceptor for SnapshotsV1Beta3.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SnapshotsV1Beta3RestTransport.

    .. code-block:: python
        class MyCustomSnapshotsV1Beta3Interceptor(SnapshotsV1Beta3RestInterceptor):
            def pre_delete_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_snapshots(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_snapshots(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SnapshotsV1Beta3RestTransport(interceptor=MyCustomSnapshotsV1Beta3Interceptor())
        client = SnapshotsV1Beta3Client(transport=transport)


    """

    def pre_delete_snapshot(
        self,
        request: snapshots.DeleteSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[snapshots.DeleteSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SnapshotsV1Beta3 server.
        """
        return request, metadata

    def post_delete_snapshot(
        self, response: snapshots.DeleteSnapshotResponse
    ) -> snapshots.DeleteSnapshotResponse:
        """Post-rpc interceptor for delete_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the SnapshotsV1Beta3 server but before
        it is returned to user code.
        """
        return response

    def pre_get_snapshot(
        self, request: snapshots.GetSnapshotRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[snapshots.GetSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SnapshotsV1Beta3 server.
        """
        return request, metadata

    def post_get_snapshot(self, response: snapshots.Snapshot) -> snapshots.Snapshot:
        """Post-rpc interceptor for get_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the SnapshotsV1Beta3 server but before
        it is returned to user code.
        """
        return response

    def pre_list_snapshots(
        self,
        request: snapshots.ListSnapshotsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[snapshots.ListSnapshotsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_snapshots

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SnapshotsV1Beta3 server.
        """
        return request, metadata

    def post_list_snapshots(
        self, response: snapshots.ListSnapshotsResponse
    ) -> snapshots.ListSnapshotsResponse:
        """Post-rpc interceptor for list_snapshots

        Override in a subclass to manipulate the response
        after it is returned by the SnapshotsV1Beta3 server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SnapshotsV1Beta3RestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SnapshotsV1Beta3RestInterceptor


class SnapshotsV1Beta3RestTransport(_BaseSnapshotsV1Beta3RestTransport):
    """REST backend synchronous transport for SnapshotsV1Beta3.

    Provides methods to manage snapshots of Google Cloud Dataflow
    jobs.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dataflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SnapshotsV1Beta3RestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dataflow.googleapis.com').
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
        self._interceptor = interceptor or SnapshotsV1Beta3RestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DeleteSnapshot(
        _BaseSnapshotsV1Beta3RestTransport._BaseDeleteSnapshot, SnapshotsV1Beta3RestStub
    ):
        def __hash__(self):
            return hash("SnapshotsV1Beta3RestTransport.DeleteSnapshot")

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
            request: snapshots.DeleteSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> snapshots.DeleteSnapshotResponse:
            r"""Call the delete snapshot method over HTTP.

            Args:
                request (~.snapshots.DeleteSnapshotRequest):
                    The request object. Request to delete a snapshot.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.snapshots.DeleteSnapshotResponse:
                    Response from deleting a snapshot.
            """

            http_options = (
                _BaseSnapshotsV1Beta3RestTransport._BaseDeleteSnapshot._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_snapshot(request, metadata)
            transcoded_request = _BaseSnapshotsV1Beta3RestTransport._BaseDeleteSnapshot._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSnapshotsV1Beta3RestTransport._BaseDeleteSnapshot._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SnapshotsV1Beta3RestTransport._DeleteSnapshot._get_response(
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
            resp = snapshots.DeleteSnapshotResponse()
            pb_resp = snapshots.DeleteSnapshotResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_snapshot(resp)
            return resp

    class _GetSnapshot(
        _BaseSnapshotsV1Beta3RestTransport._BaseGetSnapshot, SnapshotsV1Beta3RestStub
    ):
        def __hash__(self):
            return hash("SnapshotsV1Beta3RestTransport.GetSnapshot")

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
            request: snapshots.GetSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> snapshots.Snapshot:
            r"""Call the get snapshot method over HTTP.

            Args:
                request (~.snapshots.GetSnapshotRequest):
                    The request object. Request to get information about a
                snapshot
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.snapshots.Snapshot:
                    Represents a snapshot of a job.
            """

            http_options = (
                _BaseSnapshotsV1Beta3RestTransport._BaseGetSnapshot._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_snapshot(request, metadata)
            transcoded_request = _BaseSnapshotsV1Beta3RestTransport._BaseGetSnapshot._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSnapshotsV1Beta3RestTransport._BaseGetSnapshot._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SnapshotsV1Beta3RestTransport._GetSnapshot._get_response(
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
            resp = snapshots.Snapshot()
            pb_resp = snapshots.Snapshot.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_snapshot(resp)
            return resp

    class _ListSnapshots(
        _BaseSnapshotsV1Beta3RestTransport._BaseListSnapshots, SnapshotsV1Beta3RestStub
    ):
        def __hash__(self):
            return hash("SnapshotsV1Beta3RestTransport.ListSnapshots")

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
            request: snapshots.ListSnapshotsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> snapshots.ListSnapshotsResponse:
            r"""Call the list snapshots method over HTTP.

            Args:
                request (~.snapshots.ListSnapshotsRequest):
                    The request object. Request to list snapshots.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.snapshots.ListSnapshotsResponse:
                    List of snapshots.
            """

            http_options = (
                _BaseSnapshotsV1Beta3RestTransport._BaseListSnapshots._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_snapshots(request, metadata)
            transcoded_request = _BaseSnapshotsV1Beta3RestTransport._BaseListSnapshots._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSnapshotsV1Beta3RestTransport._BaseListSnapshots._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SnapshotsV1Beta3RestTransport._ListSnapshots._get_response(
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
            resp = snapshots.ListSnapshotsResponse()
            pb_resp = snapshots.ListSnapshotsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_snapshots(resp)
            return resp

    @property
    def delete_snapshot(
        self,
    ) -> Callable[[snapshots.DeleteSnapshotRequest], snapshots.DeleteSnapshotResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_snapshot(
        self,
    ) -> Callable[[snapshots.GetSnapshotRequest], snapshots.Snapshot]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_snapshots(
        self,
    ) -> Callable[[snapshots.ListSnapshotsRequest], snapshots.ListSnapshotsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSnapshots(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SnapshotsV1Beta3RestTransport",)
