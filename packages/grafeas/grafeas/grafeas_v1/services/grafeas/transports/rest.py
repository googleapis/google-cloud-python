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

from grafeas.grafeas_v1.types import grafeas

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import GrafeasTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class GrafeasRestInterceptor:
    """Interceptor for Grafeas.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the GrafeasRestTransport.

    .. code-block:: python
        class MyCustomGrafeasInterceptor(GrafeasRestInterceptor):
            def pre_batch_create_notes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_notes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_create_occurrences(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_occurrences(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_note(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_note(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_occurrence(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_occurrence(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_note(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_occurrence(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_note(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_note(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_occurrence(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_occurrence(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_occurrence_note(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_occurrence_note(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_note_occurrences(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_note_occurrences(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_notes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_notes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_occurrences(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_occurrences(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_note(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_note(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_occurrence(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_occurrence(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = GrafeasRestTransport(interceptor=MyCustomGrafeasInterceptor())
        client = GrafeasClient(transport=transport)


    """

    def pre_batch_create_notes(
        self,
        request: grafeas.BatchCreateNotesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.BatchCreateNotesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_create_notes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_batch_create_notes(
        self, response: grafeas.BatchCreateNotesResponse
    ) -> grafeas.BatchCreateNotesResponse:
        """Post-rpc interceptor for batch_create_notes

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_batch_create_occurrences(
        self,
        request: grafeas.BatchCreateOccurrencesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.BatchCreateOccurrencesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_create_occurrences

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_batch_create_occurrences(
        self, response: grafeas.BatchCreateOccurrencesResponse
    ) -> grafeas.BatchCreateOccurrencesResponse:
        """Post-rpc interceptor for batch_create_occurrences

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_create_note(
        self, request: grafeas.CreateNoteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[grafeas.CreateNoteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_note

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_create_note(self, response: grafeas.Note) -> grafeas.Note:
        """Post-rpc interceptor for create_note

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_create_occurrence(
        self,
        request: grafeas.CreateOccurrenceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.CreateOccurrenceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_occurrence

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_create_occurrence(
        self, response: grafeas.Occurrence
    ) -> grafeas.Occurrence:
        """Post-rpc interceptor for create_occurrence

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_delete_note(
        self, request: grafeas.DeleteNoteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[grafeas.DeleteNoteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_note

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def pre_delete_occurrence(
        self,
        request: grafeas.DeleteOccurrenceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.DeleteOccurrenceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_occurrence

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def pre_get_note(
        self, request: grafeas.GetNoteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[grafeas.GetNoteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_note

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_get_note(self, response: grafeas.Note) -> grafeas.Note:
        """Post-rpc interceptor for get_note

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_get_occurrence(
        self, request: grafeas.GetOccurrenceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[grafeas.GetOccurrenceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_occurrence

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_get_occurrence(self, response: grafeas.Occurrence) -> grafeas.Occurrence:
        """Post-rpc interceptor for get_occurrence

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_get_occurrence_note(
        self,
        request: grafeas.GetOccurrenceNoteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.GetOccurrenceNoteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_occurrence_note

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_get_occurrence_note(self, response: grafeas.Note) -> grafeas.Note:
        """Post-rpc interceptor for get_occurrence_note

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_list_note_occurrences(
        self,
        request: grafeas.ListNoteOccurrencesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.ListNoteOccurrencesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_note_occurrences

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_list_note_occurrences(
        self, response: grafeas.ListNoteOccurrencesResponse
    ) -> grafeas.ListNoteOccurrencesResponse:
        """Post-rpc interceptor for list_note_occurrences

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_list_notes(
        self, request: grafeas.ListNotesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[grafeas.ListNotesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_notes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_list_notes(
        self, response: grafeas.ListNotesResponse
    ) -> grafeas.ListNotesResponse:
        """Post-rpc interceptor for list_notes

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_list_occurrences(
        self,
        request: grafeas.ListOccurrencesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.ListOccurrencesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_occurrences

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_list_occurrences(
        self, response: grafeas.ListOccurrencesResponse
    ) -> grafeas.ListOccurrencesResponse:
        """Post-rpc interceptor for list_occurrences

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_update_note(
        self, request: grafeas.UpdateNoteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[grafeas.UpdateNoteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_note

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_update_note(self, response: grafeas.Note) -> grafeas.Note:
        """Post-rpc interceptor for update_note

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response

    def pre_update_occurrence(
        self,
        request: grafeas.UpdateOccurrenceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grafeas.UpdateOccurrenceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_occurrence

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Grafeas server.
        """
        return request, metadata

    def post_update_occurrence(
        self, response: grafeas.Occurrence
    ) -> grafeas.Occurrence:
        """Post-rpc interceptor for update_occurrence

        Override in a subclass to manipulate the response
        after it is returned by the Grafeas server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class GrafeasRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: GrafeasRestInterceptor


class GrafeasRestTransport(GrafeasTransport):
    """REST backend transport for Grafeas.

    `Grafeas <https://grafeas.io>`__ API.

    Retrieves analysis results of Cloud components such as Docker
    container images.

    Analysis results are stored as a series of occurrences. An
    ``Occurrence`` contains information about a specific analysis
    instance on a resource. An occurrence refers to a ``Note``. A note
    contains details describing the analysis and is generally stored in
    a separate project, called a ``Provider``. Multiple occurrences can
    refer to the same note.

    For example, an SSL vulnerability could affect multiple images. In
    this case, there would be one note for the vulnerability and an
    occurrence for each image with the vulnerability referring to that
    note.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[GrafeasRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: '').
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
        self._interceptor = interceptor or GrafeasRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchCreateNotes(GrafeasRestStub):
        def __hash__(self):
            return hash("BatchCreateNotes")

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
            request: grafeas.BatchCreateNotesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.BatchCreateNotesResponse:
            r"""Call the batch create notes method over HTTP.

            Args:
                request (~.grafeas.BatchCreateNotesRequest):
                    The request object. Request to create notes in batch.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.BatchCreateNotesResponse:
                    Response for creating notes in batch.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/notes:batchCreate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/notes:batchCreate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_create_notes(
                request, metadata
            )
            pb_request = grafeas.BatchCreateNotesRequest.pb(request)
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
            resp = grafeas.BatchCreateNotesResponse()
            pb_resp = grafeas.BatchCreateNotesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_notes(resp)
            return resp

    class _BatchCreateOccurrences(GrafeasRestStub):
        def __hash__(self):
            return hash("BatchCreateOccurrences")

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
            request: grafeas.BatchCreateOccurrencesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.BatchCreateOccurrencesResponse:
            r"""Call the batch create occurrences method over HTTP.

            Args:
                request (~.grafeas.BatchCreateOccurrencesRequest):
                    The request object. Request to create occurrences in
                batch.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.BatchCreateOccurrencesResponse:
                    Response for creating occurrences in
                batch.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/occurrences:batchCreate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/occurrences:batchCreate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_create_occurrences(
                request, metadata
            )
            pb_request = grafeas.BatchCreateOccurrencesRequest.pb(request)
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
            resp = grafeas.BatchCreateOccurrencesResponse()
            pb_resp = grafeas.BatchCreateOccurrencesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_occurrences(resp)
            return resp

    class _CreateNote(GrafeasRestStub):
        def __hash__(self):
            return hash("CreateNote")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "noteId": "",
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
            request: grafeas.CreateNoteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.Note:
            r"""Call the create note method over HTTP.

            Args:
                request (~.grafeas.CreateNoteRequest):
                    The request object. Request to create a new note.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.Note:
                    A type of analysis that can be done
                for a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/notes",
                    "body": "note",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/notes",
                    "body": "note",
                },
            ]
            request, metadata = self._interceptor.pre_create_note(request, metadata)
            pb_request = grafeas.CreateNoteRequest.pb(request)
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
            resp = grafeas.Note()
            pb_resp = grafeas.Note.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_note(resp)
            return resp

    class _CreateOccurrence(GrafeasRestStub):
        def __hash__(self):
            return hash("CreateOccurrence")

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
            request: grafeas.CreateOccurrenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.Occurrence:
            r"""Call the create occurrence method over HTTP.

            Args:
                request (~.grafeas.CreateOccurrenceRequest):
                    The request object. Request to create a new occurrence.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.Occurrence:
                    An instance of an analysis type that
                has been found on a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/occurrences",
                    "body": "occurrence",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/occurrences",
                    "body": "occurrence",
                },
            ]
            request, metadata = self._interceptor.pre_create_occurrence(
                request, metadata
            )
            pb_request = grafeas.CreateOccurrenceRequest.pb(request)
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
            resp = grafeas.Occurrence()
            pb_resp = grafeas.Occurrence.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_occurrence(resp)
            return resp

    class _DeleteNote(GrafeasRestStub):
        def __hash__(self):
            return hash("DeleteNote")

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
            request: grafeas.DeleteNoteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete note method over HTTP.

            Args:
                request (~.grafeas.DeleteNoteRequest):
                    The request object. Request to delete a note.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/notes/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/notes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_note(request, metadata)
            pb_request = grafeas.DeleteNoteRequest.pb(request)
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

    class _DeleteOccurrence(GrafeasRestStub):
        def __hash__(self):
            return hash("DeleteOccurrence")

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
            request: grafeas.DeleteOccurrenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete occurrence method over HTTP.

            Args:
                request (~.grafeas.DeleteOccurrenceRequest):
                    The request object. Request to delete an occurrence.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/occurrences/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/occurrences/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_occurrence(
                request, metadata
            )
            pb_request = grafeas.DeleteOccurrenceRequest.pb(request)
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

    class _GetNote(GrafeasRestStub):
        def __hash__(self):
            return hash("GetNote")

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
            request: grafeas.GetNoteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.Note:
            r"""Call the get note method over HTTP.

            Args:
                request (~.grafeas.GetNoteRequest):
                    The request object. Request to get a note.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.Note:
                    A type of analysis that can be done
                for a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/notes/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/notes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_note(request, metadata)
            pb_request = grafeas.GetNoteRequest.pb(request)
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
            resp = grafeas.Note()
            pb_resp = grafeas.Note.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_note(resp)
            return resp

    class _GetOccurrence(GrafeasRestStub):
        def __hash__(self):
            return hash("GetOccurrence")

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
            request: grafeas.GetOccurrenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.Occurrence:
            r"""Call the get occurrence method over HTTP.

            Args:
                request (~.grafeas.GetOccurrenceRequest):
                    The request object. Request to get an occurrence.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.Occurrence:
                    An instance of an analysis type that
                has been found on a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/occurrences/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/occurrences/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_occurrence(request, metadata)
            pb_request = grafeas.GetOccurrenceRequest.pb(request)
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
            resp = grafeas.Occurrence()
            pb_resp = grafeas.Occurrence.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_occurrence(resp)
            return resp

    class _GetOccurrenceNote(GrafeasRestStub):
        def __hash__(self):
            return hash("GetOccurrenceNote")

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
            request: grafeas.GetOccurrenceNoteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.Note:
            r"""Call the get occurrence note method over HTTP.

            Args:
                request (~.grafeas.GetOccurrenceNoteRequest):
                    The request object. Request to get the note to which the
                specified occurrence is attached.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.Note:
                    A type of analysis that can be done
                for a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/occurrences/*}/notes",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/occurrences/*}/notes",
                },
            ]
            request, metadata = self._interceptor.pre_get_occurrence_note(
                request, metadata
            )
            pb_request = grafeas.GetOccurrenceNoteRequest.pb(request)
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
            resp = grafeas.Note()
            pb_resp = grafeas.Note.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_occurrence_note(resp)
            return resp

    class _ListNoteOccurrences(GrafeasRestStub):
        def __hash__(self):
            return hash("ListNoteOccurrences")

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
            request: grafeas.ListNoteOccurrencesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.ListNoteOccurrencesResponse:
            r"""Call the list note occurrences method over HTTP.

            Args:
                request (~.grafeas.ListNoteOccurrencesRequest):
                    The request object. Request to list occurrences for a
                note.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.ListNoteOccurrencesResponse:
                    Response for listing occurrences for
                a note.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/notes/*}/occurrences",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/notes/*}/occurrences",
                },
            ]
            request, metadata = self._interceptor.pre_list_note_occurrences(
                request, metadata
            )
            pb_request = grafeas.ListNoteOccurrencesRequest.pb(request)
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
            resp = grafeas.ListNoteOccurrencesResponse()
            pb_resp = grafeas.ListNoteOccurrencesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_note_occurrences(resp)
            return resp

    class _ListNotes(GrafeasRestStub):
        def __hash__(self):
            return hash("ListNotes")

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
            request: grafeas.ListNotesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.ListNotesResponse:
            r"""Call the list notes method over HTTP.

            Args:
                request (~.grafeas.ListNotesRequest):
                    The request object. Request to list notes.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.ListNotesResponse:
                    Response for listing notes.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/notes",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/notes",
                },
            ]
            request, metadata = self._interceptor.pre_list_notes(request, metadata)
            pb_request = grafeas.ListNotesRequest.pb(request)
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
            resp = grafeas.ListNotesResponse()
            pb_resp = grafeas.ListNotesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_notes(resp)
            return resp

    class _ListOccurrences(GrafeasRestStub):
        def __hash__(self):
            return hash("ListOccurrences")

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
            request: grafeas.ListOccurrencesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.ListOccurrencesResponse:
            r"""Call the list occurrences method over HTTP.

            Args:
                request (~.grafeas.ListOccurrencesRequest):
                    The request object. Request to list occurrences.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.ListOccurrencesResponse:
                    Response for listing occurrences.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/occurrences",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/occurrences",
                },
            ]
            request, metadata = self._interceptor.pre_list_occurrences(
                request, metadata
            )
            pb_request = grafeas.ListOccurrencesRequest.pb(request)
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
            resp = grafeas.ListOccurrencesResponse()
            pb_resp = grafeas.ListOccurrencesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_occurrences(resp)
            return resp

    class _UpdateNote(GrafeasRestStub):
        def __hash__(self):
            return hash("UpdateNote")

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
            request: grafeas.UpdateNoteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.Note:
            r"""Call the update note method over HTTP.

            Args:
                request (~.grafeas.UpdateNoteRequest):
                    The request object. Request to update a note.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.Note:
                    A type of analysis that can be done
                for a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{name=projects/*/notes/*}",
                    "body": "note",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{name=projects/*/locations/*/notes/*}",
                    "body": "note",
                },
            ]
            request, metadata = self._interceptor.pre_update_note(request, metadata)
            pb_request = grafeas.UpdateNoteRequest.pb(request)
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
            resp = grafeas.Note()
            pb_resp = grafeas.Note.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_note(resp)
            return resp

    class _UpdateOccurrence(GrafeasRestStub):
        def __hash__(self):
            return hash("UpdateOccurrence")

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
            request: grafeas.UpdateOccurrenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grafeas.Occurrence:
            r"""Call the update occurrence method over HTTP.

            Args:
                request (~.grafeas.UpdateOccurrenceRequest):
                    The request object. Request to update an occurrence.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grafeas.Occurrence:
                    An instance of an analysis type that
                has been found on a resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{name=projects/*/occurrences/*}",
                    "body": "occurrence",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{name=projects/*/locations/*/occurrences/*}",
                    "body": "occurrence",
                },
            ]
            request, metadata = self._interceptor.pre_update_occurrence(
                request, metadata
            )
            pb_request = grafeas.UpdateOccurrenceRequest.pb(request)
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
            resp = grafeas.Occurrence()
            pb_resp = grafeas.Occurrence.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_occurrence(resp)
            return resp

    @property
    def batch_create_notes(
        self,
    ) -> Callable[[grafeas.BatchCreateNotesRequest], grafeas.BatchCreateNotesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateNotes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_create_occurrences(
        self,
    ) -> Callable[
        [grafeas.BatchCreateOccurrencesRequest], grafeas.BatchCreateOccurrencesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateOccurrences(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_note(self) -> Callable[[grafeas.CreateNoteRequest], grafeas.Note]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNote(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_occurrence(
        self,
    ) -> Callable[[grafeas.CreateOccurrenceRequest], grafeas.Occurrence]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateOccurrence(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_note(self) -> Callable[[grafeas.DeleteNoteRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNote(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_occurrence(
        self,
    ) -> Callable[[grafeas.DeleteOccurrenceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteOccurrence(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_note(self) -> Callable[[grafeas.GetNoteRequest], grafeas.Note]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNote(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_occurrence(
        self,
    ) -> Callable[[grafeas.GetOccurrenceRequest], grafeas.Occurrence]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOccurrence(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_occurrence_note(
        self,
    ) -> Callable[[grafeas.GetOccurrenceNoteRequest], grafeas.Note]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOccurrenceNote(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_note_occurrences(
        self,
    ) -> Callable[
        [grafeas.ListNoteOccurrencesRequest], grafeas.ListNoteOccurrencesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNoteOccurrences(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_notes(
        self,
    ) -> Callable[[grafeas.ListNotesRequest], grafeas.ListNotesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNotes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_occurrences(
        self,
    ) -> Callable[[grafeas.ListOccurrencesRequest], grafeas.ListOccurrencesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOccurrences(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_note(self) -> Callable[[grafeas.UpdateNoteRequest], grafeas.Note]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNote(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_occurrence(
        self,
    ) -> Callable[[grafeas.UpdateOccurrenceRequest], grafeas.Occurrence]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateOccurrence(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("GrafeasRestTransport",)
