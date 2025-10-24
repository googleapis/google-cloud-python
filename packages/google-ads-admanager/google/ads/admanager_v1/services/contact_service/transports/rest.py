# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.longrunning import operations_pb2  # type: ignore
import google.protobuf
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.ads.admanager_v1.types import contact_messages, contact_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseContactServiceRestTransport

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

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class ContactServiceRestInterceptor:
    """Interceptor for ContactService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ContactServiceRestTransport.

    .. code-block:: python
        class MyCustomContactServiceInterceptor(ContactServiceRestInterceptor):
            def pre_batch_create_contacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_contacts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_update_contacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_contacts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_contact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_contact(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_contact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_contact(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_contacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_contacts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_contact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_contact(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ContactServiceRestTransport(interceptor=MyCustomContactServiceInterceptor())
        client = ContactServiceClient(transport=transport)


    """

    def pre_batch_create_contacts(
        self,
        request: contact_service.BatchCreateContactsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.BatchCreateContactsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for batch_create_contacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactService server.
        """
        return request, metadata

    def post_batch_create_contacts(
        self, response: contact_service.BatchCreateContactsResponse
    ) -> contact_service.BatchCreateContactsResponse:
        """Post-rpc interceptor for batch_create_contacts

        DEPRECATED. Please use the `post_batch_create_contacts_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContactService server but before
        it is returned to user code. This `post_batch_create_contacts` interceptor runs
        before the `post_batch_create_contacts_with_metadata` interceptor.
        """
        return response

    def post_batch_create_contacts_with_metadata(
        self,
        response: contact_service.BatchCreateContactsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.BatchCreateContactsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for batch_create_contacts

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContactService server but before it is returned to user code.

        We recommend only using this `post_batch_create_contacts_with_metadata`
        interceptor in new development instead of the `post_batch_create_contacts` interceptor.
        When both interceptors are used, this `post_batch_create_contacts_with_metadata` interceptor runs after the
        `post_batch_create_contacts` interceptor. The (possibly modified) response returned by
        `post_batch_create_contacts` will be passed to
        `post_batch_create_contacts_with_metadata`.
        """
        return response, metadata

    def pre_batch_update_contacts(
        self,
        request: contact_service.BatchUpdateContactsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.BatchUpdateContactsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for batch_update_contacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactService server.
        """
        return request, metadata

    def post_batch_update_contacts(
        self, response: contact_service.BatchUpdateContactsResponse
    ) -> contact_service.BatchUpdateContactsResponse:
        """Post-rpc interceptor for batch_update_contacts

        DEPRECATED. Please use the `post_batch_update_contacts_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContactService server but before
        it is returned to user code. This `post_batch_update_contacts` interceptor runs
        before the `post_batch_update_contacts_with_metadata` interceptor.
        """
        return response

    def post_batch_update_contacts_with_metadata(
        self,
        response: contact_service.BatchUpdateContactsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.BatchUpdateContactsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for batch_update_contacts

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContactService server but before it is returned to user code.

        We recommend only using this `post_batch_update_contacts_with_metadata`
        interceptor in new development instead of the `post_batch_update_contacts` interceptor.
        When both interceptors are used, this `post_batch_update_contacts_with_metadata` interceptor runs after the
        `post_batch_update_contacts` interceptor. The (possibly modified) response returned by
        `post_batch_update_contacts` will be passed to
        `post_batch_update_contacts_with_metadata`.
        """
        return response, metadata

    def pre_create_contact(
        self,
        request: contact_service.CreateContactRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.CreateContactRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_contact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactService server.
        """
        return request, metadata

    def post_create_contact(
        self, response: contact_messages.Contact
    ) -> contact_messages.Contact:
        """Post-rpc interceptor for create_contact

        DEPRECATED. Please use the `post_create_contact_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContactService server but before
        it is returned to user code. This `post_create_contact` interceptor runs
        before the `post_create_contact_with_metadata` interceptor.
        """
        return response

    def post_create_contact_with_metadata(
        self,
        response: contact_messages.Contact,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[contact_messages.Contact, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_contact

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContactService server but before it is returned to user code.

        We recommend only using this `post_create_contact_with_metadata`
        interceptor in new development instead of the `post_create_contact` interceptor.
        When both interceptors are used, this `post_create_contact_with_metadata` interceptor runs after the
        `post_create_contact` interceptor. The (possibly modified) response returned by
        `post_create_contact` will be passed to
        `post_create_contact_with_metadata`.
        """
        return response, metadata

    def pre_get_contact(
        self,
        request: contact_service.GetContactRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.GetContactRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_contact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactService server.
        """
        return request, metadata

    def post_get_contact(
        self, response: contact_messages.Contact
    ) -> contact_messages.Contact:
        """Post-rpc interceptor for get_contact

        DEPRECATED. Please use the `post_get_contact_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContactService server but before
        it is returned to user code. This `post_get_contact` interceptor runs
        before the `post_get_contact_with_metadata` interceptor.
        """
        return response

    def post_get_contact_with_metadata(
        self,
        response: contact_messages.Contact,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[contact_messages.Contact, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_contact

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContactService server but before it is returned to user code.

        We recommend only using this `post_get_contact_with_metadata`
        interceptor in new development instead of the `post_get_contact` interceptor.
        When both interceptors are used, this `post_get_contact_with_metadata` interceptor runs after the
        `post_get_contact` interceptor. The (possibly modified) response returned by
        `post_get_contact` will be passed to
        `post_get_contact_with_metadata`.
        """
        return response, metadata

    def pre_list_contacts(
        self,
        request: contact_service.ListContactsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.ListContactsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_contacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactService server.
        """
        return request, metadata

    def post_list_contacts(
        self, response: contact_service.ListContactsResponse
    ) -> contact_service.ListContactsResponse:
        """Post-rpc interceptor for list_contacts

        DEPRECATED. Please use the `post_list_contacts_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContactService server but before
        it is returned to user code. This `post_list_contacts` interceptor runs
        before the `post_list_contacts_with_metadata` interceptor.
        """
        return response

    def post_list_contacts_with_metadata(
        self,
        response: contact_service.ListContactsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.ListContactsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_contacts

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContactService server but before it is returned to user code.

        We recommend only using this `post_list_contacts_with_metadata`
        interceptor in new development instead of the `post_list_contacts` interceptor.
        When both interceptors are used, this `post_list_contacts_with_metadata` interceptor runs after the
        `post_list_contacts` interceptor. The (possibly modified) response returned by
        `post_list_contacts` will be passed to
        `post_list_contacts_with_metadata`.
        """
        return response, metadata

    def pre_update_contact(
        self,
        request: contact_service.UpdateContactRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        contact_service.UpdateContactRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_contact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactService server.
        """
        return request, metadata

    def post_update_contact(
        self, response: contact_messages.Contact
    ) -> contact_messages.Contact:
        """Post-rpc interceptor for update_contact

        DEPRECATED. Please use the `post_update_contact_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContactService server but before
        it is returned to user code. This `post_update_contact` interceptor runs
        before the `post_update_contact_with_metadata` interceptor.
        """
        return response

    def post_update_contact_with_metadata(
        self,
        response: contact_messages.Contact,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[contact_messages.Contact, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_contact

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContactService server but before it is returned to user code.

        We recommend only using this `post_update_contact_with_metadata`
        interceptor in new development instead of the `post_update_contact` interceptor.
        When both interceptors are used, this `post_update_contact_with_metadata` interceptor runs after the
        `post_update_contact` interceptor. The (possibly modified) response returned by
        `post_update_contact` will be passed to
        `post_update_contact_with_metadata`.
        """
        return response, metadata

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ContactService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ContactServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ContactServiceRestInterceptor


class ContactServiceRestTransport(_BaseContactServiceRestTransport):
    """REST backend synchronous transport for ContactService.

    Provides methods for handling ``Contact`` objects.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "admanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ContactServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'admanager.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
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
        self._interceptor = interceptor or ContactServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchCreateContacts(
        _BaseContactServiceRestTransport._BaseBatchCreateContacts,
        ContactServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContactServiceRestTransport.BatchCreateContacts")

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
            request: contact_service.BatchCreateContactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> contact_service.BatchCreateContactsResponse:
            r"""Call the batch create contacts method over HTTP.

            Args:
                request (~.contact_service.BatchCreateContactsRequest):
                    The request object. Request object for ``BatchCreateContacts`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.contact_service.BatchCreateContactsResponse:
                    Response object for ``BatchCreateContacts`` method.
            """

            http_options = (
                _BaseContactServiceRestTransport._BaseBatchCreateContacts._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_create_contacts(
                request, metadata
            )
            transcoded_request = _BaseContactServiceRestTransport._BaseBatchCreateContacts._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactServiceRestTransport._BaseBatchCreateContacts._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactServiceRestTransport._BaseBatchCreateContacts._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContactServiceClient.BatchCreateContacts",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "BatchCreateContacts",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContactServiceRestTransport._BatchCreateContacts._get_response(
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
            resp = contact_service.BatchCreateContactsResponse()
            pb_resp = contact_service.BatchCreateContactsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_batch_create_contacts(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_batch_create_contacts_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        contact_service.BatchCreateContactsResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.admanager_v1.ContactServiceClient.batch_create_contacts",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "BatchCreateContacts",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _BatchUpdateContacts(
        _BaseContactServiceRestTransport._BaseBatchUpdateContacts,
        ContactServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContactServiceRestTransport.BatchUpdateContacts")

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
            request: contact_service.BatchUpdateContactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> contact_service.BatchUpdateContactsResponse:
            r"""Call the batch update contacts method over HTTP.

            Args:
                request (~.contact_service.BatchUpdateContactsRequest):
                    The request object. Request object for ``BatchUpdateContacts`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.contact_service.BatchUpdateContactsResponse:
                    Response object for ``BatchUpdateContacts`` method.
            """

            http_options = (
                _BaseContactServiceRestTransport._BaseBatchUpdateContacts._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_update_contacts(
                request, metadata
            )
            transcoded_request = _BaseContactServiceRestTransport._BaseBatchUpdateContacts._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactServiceRestTransport._BaseBatchUpdateContacts._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactServiceRestTransport._BaseBatchUpdateContacts._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContactServiceClient.BatchUpdateContacts",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "BatchUpdateContacts",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContactServiceRestTransport._BatchUpdateContacts._get_response(
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
            resp = contact_service.BatchUpdateContactsResponse()
            pb_resp = contact_service.BatchUpdateContactsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_batch_update_contacts(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_batch_update_contacts_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        contact_service.BatchUpdateContactsResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.admanager_v1.ContactServiceClient.batch_update_contacts",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "BatchUpdateContacts",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateContact(
        _BaseContactServiceRestTransport._BaseCreateContact, ContactServiceRestStub
    ):
        def __hash__(self):
            return hash("ContactServiceRestTransport.CreateContact")

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
            request: contact_service.CreateContactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> contact_messages.Contact:
            r"""Call the create contact method over HTTP.

            Args:
                request (~.contact_service.CreateContactRequest):
                    The request object. Request object for ``CreateContact`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.contact_messages.Contact:
                    A contact represents a person who is
                affiliated with a single company. A
                contact can have a variety of contact
                information associated to it, and can be
                invited to view their company's orders,
                line items, creatives, and reports.

            """

            http_options = (
                _BaseContactServiceRestTransport._BaseCreateContact._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_contact(request, metadata)
            transcoded_request = _BaseContactServiceRestTransport._BaseCreateContact._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactServiceRestTransport._BaseCreateContact._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactServiceRestTransport._BaseCreateContact._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContactServiceClient.CreateContact",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "CreateContact",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContactServiceRestTransport._CreateContact._get_response(
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
            resp = contact_messages.Contact()
            pb_resp = contact_messages.Contact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_contact(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_contact_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = contact_messages.Contact.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.admanager_v1.ContactServiceClient.create_contact",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "CreateContact",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetContact(
        _BaseContactServiceRestTransport._BaseGetContact, ContactServiceRestStub
    ):
        def __hash__(self):
            return hash("ContactServiceRestTransport.GetContact")

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
            request: contact_service.GetContactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> contact_messages.Contact:
            r"""Call the get contact method over HTTP.

            Args:
                request (~.contact_service.GetContactRequest):
                    The request object. Request object for ``GetContact`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.contact_messages.Contact:
                    A contact represents a person who is
                affiliated with a single company. A
                contact can have a variety of contact
                information associated to it, and can be
                invited to view their company's orders,
                line items, creatives, and reports.

            """

            http_options = (
                _BaseContactServiceRestTransport._BaseGetContact._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_contact(request, metadata)
            transcoded_request = _BaseContactServiceRestTransport._BaseGetContact._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseContactServiceRestTransport._BaseGetContact._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.ads.admanager_v1.ContactServiceClient.GetContact",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "GetContact",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContactServiceRestTransport._GetContact._get_response(
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
            resp = contact_messages.Contact()
            pb_resp = contact_messages.Contact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_contact(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_contact_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = contact_messages.Contact.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.admanager_v1.ContactServiceClient.get_contact",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "GetContact",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListContacts(
        _BaseContactServiceRestTransport._BaseListContacts, ContactServiceRestStub
    ):
        def __hash__(self):
            return hash("ContactServiceRestTransport.ListContacts")

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
            request: contact_service.ListContactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> contact_service.ListContactsResponse:
            r"""Call the list contacts method over HTTP.

            Args:
                request (~.contact_service.ListContactsRequest):
                    The request object. Request object for ``ListContacts`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.contact_service.ListContactsResponse:
                    Response object for ``ListContactsRequest`` containing
                matching ``Contact`` objects.

            """

            http_options = (
                _BaseContactServiceRestTransport._BaseListContacts._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_contacts(request, metadata)
            transcoded_request = _BaseContactServiceRestTransport._BaseListContacts._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactServiceRestTransport._BaseListContacts._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContactServiceClient.ListContacts",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "ListContacts",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContactServiceRestTransport._ListContacts._get_response(
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
            resp = contact_service.ListContactsResponse()
            pb_resp = contact_service.ListContactsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_contacts(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_contacts_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = contact_service.ListContactsResponse.to_json(
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
                    "Received response for google.ads.admanager_v1.ContactServiceClient.list_contacts",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "ListContacts",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateContact(
        _BaseContactServiceRestTransport._BaseUpdateContact, ContactServiceRestStub
    ):
        def __hash__(self):
            return hash("ContactServiceRestTransport.UpdateContact")

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
            request: contact_service.UpdateContactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> contact_messages.Contact:
            r"""Call the update contact method over HTTP.

            Args:
                request (~.contact_service.UpdateContactRequest):
                    The request object. Request object for ``UpdateContact`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.contact_messages.Contact:
                    A contact represents a person who is
                affiliated with a single company. A
                contact can have a variety of contact
                information associated to it, and can be
                invited to view their company's orders,
                line items, creatives, and reports.

            """

            http_options = (
                _BaseContactServiceRestTransport._BaseUpdateContact._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_contact(request, metadata)
            transcoded_request = _BaseContactServiceRestTransport._BaseUpdateContact._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactServiceRestTransport._BaseUpdateContact._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactServiceRestTransport._BaseUpdateContact._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContactServiceClient.UpdateContact",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "UpdateContact",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContactServiceRestTransport._UpdateContact._get_response(
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
            resp = contact_messages.Contact()
            pb_resp = contact_messages.Contact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_contact(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_contact_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = contact_messages.Contact.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.admanager_v1.ContactServiceClient.update_contact",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "UpdateContact",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def batch_create_contacts(
        self,
    ) -> Callable[
        [contact_service.BatchCreateContactsRequest],
        contact_service.BatchCreateContactsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateContacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_contacts(
        self,
    ) -> Callable[
        [contact_service.BatchUpdateContactsRequest],
        contact_service.BatchUpdateContactsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateContacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_contact(
        self,
    ) -> Callable[[contact_service.CreateContactRequest], contact_messages.Contact]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateContact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_contact(
        self,
    ) -> Callable[[contact_service.GetContactRequest], contact_messages.Contact]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetContact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_contacts(
        self,
    ) -> Callable[
        [contact_service.ListContactsRequest], contact_service.ListContactsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListContacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_contact(
        self,
    ) -> Callable[[contact_service.UpdateContactRequest], contact_messages.Contact]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateContact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseContactServiceRestTransport._BaseGetOperation, ContactServiceRestStub
    ):
        def __hash__(self):
            return hash("ContactServiceRestTransport.GetOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseContactServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseContactServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactServiceRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.ads.admanager_v1.ContactServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContactServiceRestTransport._GetOperation._get_response(
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
                    "Received response for google.ads.admanager_v1.ContactServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.ads.admanager.v1.ContactService",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ContactServiceRestTransport",)
