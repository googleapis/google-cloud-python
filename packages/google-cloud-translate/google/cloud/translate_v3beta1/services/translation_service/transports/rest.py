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

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
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


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.translate_v3beta1.types import translation_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import TranslationServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class TranslationServiceRestInterceptor:
    """Interceptor for TranslationService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the TranslationServiceRestTransport.

    .. code-block:: python
        class MyCustomTranslationServiceInterceptor(TranslationServiceRestInterceptor):
            def pre_batch_translate_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_translate_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_translate_text(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_translate_text(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_glossary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_glossary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_glossary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_glossary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_detect_language(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_detect_language(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_glossary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_glossary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_supported_languages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_supported_languages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_glossaries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_glossaries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_translate_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_translate_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_translate_text(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_translate_text(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = TranslationServiceRestTransport(interceptor=MyCustomTranslationServiceInterceptor())
        client = TranslationServiceClient(transport=transport)


    """

    def pre_batch_translate_document(
        self,
        request: translation_service.BatchTranslateDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        translation_service.BatchTranslateDocumentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_translate_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_batch_translate_document(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_translate_document

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_batch_translate_text(
        self,
        request: translation_service.BatchTranslateTextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        translation_service.BatchTranslateTextRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_translate_text

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_batch_translate_text(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_translate_text

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_create_glossary(
        self,
        request: translation_service.CreateGlossaryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.CreateGlossaryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_glossary

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_create_glossary(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_glossary

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_glossary(
        self,
        request: translation_service.DeleteGlossaryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.DeleteGlossaryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_glossary

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_delete_glossary(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_glossary

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_detect_language(
        self,
        request: translation_service.DetectLanguageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.DetectLanguageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for detect_language

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_detect_language(
        self, response: translation_service.DetectLanguageResponse
    ) -> translation_service.DetectLanguageResponse:
        """Post-rpc interceptor for detect_language

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_glossary(
        self,
        request: translation_service.GetGlossaryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.GetGlossaryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_glossary

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_glossary(
        self, response: translation_service.Glossary
    ) -> translation_service.Glossary:
        """Post-rpc interceptor for get_glossary

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_supported_languages(
        self,
        request: translation_service.GetSupportedLanguagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        translation_service.GetSupportedLanguagesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_supported_languages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_supported_languages(
        self, response: translation_service.SupportedLanguages
    ) -> translation_service.SupportedLanguages:
        """Post-rpc interceptor for get_supported_languages

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_glossaries(
        self,
        request: translation_service.ListGlossariesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.ListGlossariesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_glossaries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_glossaries(
        self, response: translation_service.ListGlossariesResponse
    ) -> translation_service.ListGlossariesResponse:
        """Post-rpc interceptor for list_glossaries

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_translate_document(
        self,
        request: translation_service.TranslateDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.TranslateDocumentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for translate_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_translate_document(
        self, response: translation_service.TranslateDocumentResponse
    ) -> translation_service.TranslateDocumentResponse:
        """Post-rpc interceptor for translate_document

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_translate_text(
        self,
        request: translation_service.TranslateTextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.TranslateTextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for translate_text

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_translate_text(
        self, response: translation_service.TranslateTextResponse
    ) -> translation_service.TranslateTextResponse:
        """Post-rpc interceptor for translate_text

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class TranslationServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: TranslationServiceRestInterceptor


class TranslationServiceRestTransport(TranslationServiceTransport):
    """REST backend transport for TranslationService.

    Provides natural language translation operations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "translate.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[TranslationServiceRestInterceptor] = None,
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or TranslationServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v3beta1/{name=projects/*/locations/*}/operations",
                    },
                ],
                "google.longrunning.Operations.WaitOperation": [
                    {
                        "method": "post",
                        "uri": "/v3beta1/{name=projects/*/locations/*/operations/*}:wait",
                        "body": "*",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v3beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchTranslateDocument(TranslationServiceRestStub):
        def __hash__(self):
            return hash("BatchTranslateDocument")

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
            request: translation_service.BatchTranslateDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch translate document method over HTTP.

            Args:
                request (~.translation_service.BatchTranslateDocumentRequest):
                    The request object. The BatchTranslateDocument request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}:batchTranslateDocument",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_translate_document(
                request, metadata
            )
            pb_request = translation_service.BatchTranslateDocumentRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_translate_document(resp)
            return resp

    class _BatchTranslateText(TranslationServiceRestStub):
        def __hash__(self):
            return hash("BatchTranslateText")

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
            request: translation_service.BatchTranslateTextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch translate text method over HTTP.

            Args:
                request (~.translation_service.BatchTranslateTextRequest):
                    The request object. The batch translation request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}:batchTranslateText",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_translate_text(
                request, metadata
            )
            pb_request = translation_service.BatchTranslateTextRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_translate_text(resp)
            return resp

    class _CreateGlossary(TranslationServiceRestStub):
        def __hash__(self):
            return hash("CreateGlossary")

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
            request: translation_service.CreateGlossaryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create glossary method over HTTP.

            Args:
                request (~.translation_service.CreateGlossaryRequest):
                    The request object. Request message for CreateGlossary.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}/glossaries",
                    "body": "glossary",
                },
            ]
            request, metadata = self._interceptor.pre_create_glossary(request, metadata)
            pb_request = translation_service.CreateGlossaryRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_glossary(resp)
            return resp

    class _DeleteGlossary(TranslationServiceRestStub):
        def __hash__(self):
            return hash("DeleteGlossary")

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
            request: translation_service.DeleteGlossaryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete glossary method over HTTP.

            Args:
                request (~.translation_service.DeleteGlossaryRequest):
                    The request object. Request message for DeleteGlossary.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3beta1/{name=projects/*/locations/*/glossaries/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_glossary(request, metadata)
            pb_request = translation_service.DeleteGlossaryRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_glossary(resp)
            return resp

    class _DetectLanguage(TranslationServiceRestStub):
        def __hash__(self):
            return hash("DetectLanguage")

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
            request: translation_service.DetectLanguageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.DetectLanguageResponse:
            r"""Call the detect language method over HTTP.

            Args:
                request (~.translation_service.DetectLanguageRequest):
                    The request object. The request message for language
                detection.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.DetectLanguageResponse:
                    The response message for language
                detection.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}:detectLanguage",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*}:detectLanguage",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_detect_language(request, metadata)
            pb_request = translation_service.DetectLanguageRequest.pb(request)
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
            resp = translation_service.DetectLanguageResponse()
            pb_resp = translation_service.DetectLanguageResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_detect_language(resp)
            return resp

    class _GetGlossary(TranslationServiceRestStub):
        def __hash__(self):
            return hash("GetGlossary")

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
            request: translation_service.GetGlossaryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.Glossary:
            r"""Call the get glossary method over HTTP.

            Args:
                request (~.translation_service.GetGlossaryRequest):
                    The request object. Request message for GetGlossary.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.Glossary:
                    Represents a glossary built from user
                provided data.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3beta1/{name=projects/*/locations/*/glossaries/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_glossary(request, metadata)
            pb_request = translation_service.GetGlossaryRequest.pb(request)
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
            resp = translation_service.Glossary()
            pb_resp = translation_service.Glossary.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_glossary(resp)
            return resp

    class _GetSupportedLanguages(TranslationServiceRestStub):
        def __hash__(self):
            return hash("GetSupportedLanguages")

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
            request: translation_service.GetSupportedLanguagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.SupportedLanguages:
            r"""Call the get supported languages method over HTTP.

            Args:
                request (~.translation_service.GetSupportedLanguagesRequest):
                    The request object. The request message for discovering
                supported languages.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.SupportedLanguages:
                    The response message for discovering
                supported languages.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}/supportedLanguages",
                },
                {
                    "method": "get",
                    "uri": "/v3beta1/{parent=projects/*}/supportedLanguages",
                },
            ]
            request, metadata = self._interceptor.pre_get_supported_languages(
                request, metadata
            )
            pb_request = translation_service.GetSupportedLanguagesRequest.pb(request)
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
            resp = translation_service.SupportedLanguages()
            pb_resp = translation_service.SupportedLanguages.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_supported_languages(resp)
            return resp

    class _ListGlossaries(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ListGlossaries")

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
            request: translation_service.ListGlossariesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.ListGlossariesResponse:
            r"""Call the list glossaries method over HTTP.

            Args:
                request (~.translation_service.ListGlossariesRequest):
                    The request object. Request message for ListGlossaries.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.ListGlossariesResponse:
                    Response message for ListGlossaries.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}/glossaries",
                },
            ]
            request, metadata = self._interceptor.pre_list_glossaries(request, metadata)
            pb_request = translation_service.ListGlossariesRequest.pb(request)
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
            resp = translation_service.ListGlossariesResponse()
            pb_resp = translation_service.ListGlossariesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_glossaries(resp)
            return resp

    class _TranslateDocument(TranslationServiceRestStub):
        def __hash__(self):
            return hash("TranslateDocument")

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
            request: translation_service.TranslateDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.TranslateDocumentResponse:
            r"""Call the translate document method over HTTP.

            Args:
                request (~.translation_service.TranslateDocumentRequest):
                    The request object. A document translation request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.TranslateDocumentResponse:
                    A translated document response
                message.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}:translateDocument",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_translate_document(
                request, metadata
            )
            pb_request = translation_service.TranslateDocumentRequest.pb(request)
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
            resp = translation_service.TranslateDocumentResponse()
            pb_resp = translation_service.TranslateDocumentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_translate_document(resp)
            return resp

    class _TranslateText(TranslationServiceRestStub):
        def __hash__(self):
            return hash("TranslateText")

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
            request: translation_service.TranslateTextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.TranslateTextResponse:
            r"""Call the translate text method over HTTP.

            Args:
                request (~.translation_service.TranslateTextRequest):
                    The request object. The request message for synchronous
                translation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.TranslateTextResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*/locations/*}:translateText",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v3beta1/{parent=projects/*}:translateText",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_translate_text(request, metadata)
            pb_request = translation_service.TranslateTextRequest.pb(request)
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
            resp = translation_service.TranslateTextResponse()
            pb_resp = translation_service.TranslateTextResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_translate_text(resp)
            return resp

    @property
    def batch_translate_document(
        self,
    ) -> Callable[
        [translation_service.BatchTranslateDocumentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchTranslateDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_translate_text(
        self,
    ) -> Callable[
        [translation_service.BatchTranslateTextRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchTranslateText(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_glossary(
        self,
    ) -> Callable[
        [translation_service.CreateGlossaryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGlossary(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_glossary(
        self,
    ) -> Callable[
        [translation_service.DeleteGlossaryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGlossary(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def detect_language(
        self,
    ) -> Callable[
        [translation_service.DetectLanguageRequest],
        translation_service.DetectLanguageResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DetectLanguage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_glossary(
        self,
    ) -> Callable[
        [translation_service.GetGlossaryRequest], translation_service.Glossary
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGlossary(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_supported_languages(
        self,
    ) -> Callable[
        [translation_service.GetSupportedLanguagesRequest],
        translation_service.SupportedLanguages,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSupportedLanguages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_glossaries(
        self,
    ) -> Callable[
        [translation_service.ListGlossariesRequest],
        translation_service.ListGlossariesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGlossaries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def translate_document(
        self,
    ) -> Callable[
        [translation_service.TranslateDocumentRequest],
        translation_service.TranslateDocumentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TranslateDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def translate_text(
        self,
    ) -> Callable[
        [translation_service.TranslateTextRequest],
        translation_service.TranslateTextResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TranslateText(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("TranslationServiceRestTransport",)
