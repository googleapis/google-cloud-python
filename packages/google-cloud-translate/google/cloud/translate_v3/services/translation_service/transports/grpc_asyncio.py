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
import inspect
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.translate_v3.types import (
    adaptive_mt,
    automl_translation,
    common,
    translation_service,
)

from .base import DEFAULT_CLIENT_INFO, TranslationServiceTransport
from .grpc import TranslationServiceGrpcTransport


class TranslationServiceGrpcAsyncIOTransport(TranslationServiceTransport):
    """gRPC AsyncIO backend transport for TranslationService.

    Provides natural language translation operations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "translate.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "translate.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'translate.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, aio.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def translate_text(
        self,
    ) -> Callable[
        [translation_service.TranslateTextRequest],
        Awaitable[translation_service.TranslateTextResponse],
    ]:
        r"""Return a callable for the translate text method over gRPC.

        Translates input text and returns translated text.

        Returns:
            Callable[[~.TranslateTextRequest],
                    Awaitable[~.TranslateTextResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "translate_text" not in self._stubs:
            self._stubs["translate_text"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/TranslateText",
                request_serializer=translation_service.TranslateTextRequest.serialize,
                response_deserializer=translation_service.TranslateTextResponse.deserialize,
            )
        return self._stubs["translate_text"]

    @property
    def romanize_text(
        self,
    ) -> Callable[
        [translation_service.RomanizeTextRequest],
        Awaitable[translation_service.RomanizeTextResponse],
    ]:
        r"""Return a callable for the romanize text method over gRPC.

        Romanize input text written in non-Latin scripts to
        Latin text.

        Returns:
            Callable[[~.RomanizeTextRequest],
                    Awaitable[~.RomanizeTextResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "romanize_text" not in self._stubs:
            self._stubs["romanize_text"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/RomanizeText",
                request_serializer=translation_service.RomanizeTextRequest.serialize,
                response_deserializer=translation_service.RomanizeTextResponse.deserialize,
            )
        return self._stubs["romanize_text"]

    @property
    def detect_language(
        self,
    ) -> Callable[
        [translation_service.DetectLanguageRequest],
        Awaitable[translation_service.DetectLanguageResponse],
    ]:
        r"""Return a callable for the detect language method over gRPC.

        Detects the language of text within a request.

        Returns:
            Callable[[~.DetectLanguageRequest],
                    Awaitable[~.DetectLanguageResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "detect_language" not in self._stubs:
            self._stubs["detect_language"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/DetectLanguage",
                request_serializer=translation_service.DetectLanguageRequest.serialize,
                response_deserializer=translation_service.DetectLanguageResponse.deserialize,
            )
        return self._stubs["detect_language"]

    @property
    def get_supported_languages(
        self,
    ) -> Callable[
        [translation_service.GetSupportedLanguagesRequest],
        Awaitable[translation_service.SupportedLanguages],
    ]:
        r"""Return a callable for the get supported languages method over gRPC.

        Returns a list of supported languages for
        translation.

        Returns:
            Callable[[~.GetSupportedLanguagesRequest],
                    Awaitable[~.SupportedLanguages]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_supported_languages" not in self._stubs:
            self._stubs["get_supported_languages"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/GetSupportedLanguages",
                request_serializer=translation_service.GetSupportedLanguagesRequest.serialize,
                response_deserializer=translation_service.SupportedLanguages.deserialize,
            )
        return self._stubs["get_supported_languages"]

    @property
    def translate_document(
        self,
    ) -> Callable[
        [translation_service.TranslateDocumentRequest],
        Awaitable[translation_service.TranslateDocumentResponse],
    ]:
        r"""Return a callable for the translate document method over gRPC.

        Translates documents in synchronous mode.

        Returns:
            Callable[[~.TranslateDocumentRequest],
                    Awaitable[~.TranslateDocumentResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "translate_document" not in self._stubs:
            self._stubs["translate_document"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/TranslateDocument",
                request_serializer=translation_service.TranslateDocumentRequest.serialize,
                response_deserializer=translation_service.TranslateDocumentResponse.deserialize,
            )
        return self._stubs["translate_document"]

    @property
    def batch_translate_text(
        self,
    ) -> Callable[
        [translation_service.BatchTranslateTextRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch translate text method over gRPC.

        Translates a large volume of text in asynchronous
        batch mode. This function provides real-time output as
        the inputs are being processed. If caller cancels a
        request, the partial results (for an input file, it's
        all or nothing) may still be available on the specified
        output location.

        This call returns immediately and you can
        use google.longrunning.Operation.name to poll the status
        of the call.

        Returns:
            Callable[[~.BatchTranslateTextRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_translate_text" not in self._stubs:
            self._stubs["batch_translate_text"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/BatchTranslateText",
                request_serializer=translation_service.BatchTranslateTextRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_translate_text"]

    @property
    def batch_translate_document(
        self,
    ) -> Callable[
        [translation_service.BatchTranslateDocumentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch translate document method over gRPC.

        Translates a large volume of document in asynchronous
        batch mode. This function provides real-time output as
        the inputs are being processed. If caller cancels a
        request, the partial results (for an input file, it's
        all or nothing) may still be available on the specified
        output location.

        This call returns immediately and you can use
        google.longrunning.Operation.name to poll the status of
        the call.

        Returns:
            Callable[[~.BatchTranslateDocumentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_translate_document" not in self._stubs:
            self._stubs["batch_translate_document"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/BatchTranslateDocument",
                request_serializer=translation_service.BatchTranslateDocumentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_translate_document"]

    @property
    def create_glossary(
        self,
    ) -> Callable[
        [translation_service.CreateGlossaryRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create glossary method over gRPC.

        Creates a glossary and returns the long-running operation.
        Returns NOT_FOUND, if the project doesn't exist.

        Returns:
            Callable[[~.CreateGlossaryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_glossary" not in self._stubs:
            self._stubs["create_glossary"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/CreateGlossary",
                request_serializer=translation_service.CreateGlossaryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_glossary"]

    @property
    def update_glossary(
        self,
    ) -> Callable[
        [translation_service.UpdateGlossaryRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update glossary method over gRPC.

        Updates a glossary. A LRO is used since the update
        can be async if the glossary's entry file is updated.

        Returns:
            Callable[[~.UpdateGlossaryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_glossary" not in self._stubs:
            self._stubs["update_glossary"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/UpdateGlossary",
                request_serializer=translation_service.UpdateGlossaryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_glossary"]

    @property
    def list_glossaries(
        self,
    ) -> Callable[
        [translation_service.ListGlossariesRequest],
        Awaitable[translation_service.ListGlossariesResponse],
    ]:
        r"""Return a callable for the list glossaries method over gRPC.

        Lists glossaries in a project. Returns NOT_FOUND, if the project
        doesn't exist.

        Returns:
            Callable[[~.ListGlossariesRequest],
                    Awaitable[~.ListGlossariesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_glossaries" not in self._stubs:
            self._stubs["list_glossaries"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListGlossaries",
                request_serializer=translation_service.ListGlossariesRequest.serialize,
                response_deserializer=translation_service.ListGlossariesResponse.deserialize,
            )
        return self._stubs["list_glossaries"]

    @property
    def get_glossary(
        self,
    ) -> Callable[
        [translation_service.GetGlossaryRequest],
        Awaitable[translation_service.Glossary],
    ]:
        r"""Return a callable for the get glossary method over gRPC.

        Gets a glossary. Returns NOT_FOUND, if the glossary doesn't
        exist.

        Returns:
            Callable[[~.GetGlossaryRequest],
                    Awaitable[~.Glossary]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_glossary" not in self._stubs:
            self._stubs["get_glossary"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/GetGlossary",
                request_serializer=translation_service.GetGlossaryRequest.serialize,
                response_deserializer=translation_service.Glossary.deserialize,
            )
        return self._stubs["get_glossary"]

    @property
    def delete_glossary(
        self,
    ) -> Callable[
        [translation_service.DeleteGlossaryRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete glossary method over gRPC.

        Deletes a glossary, or cancels glossary construction if the
        glossary isn't created yet. Returns NOT_FOUND, if the glossary
        doesn't exist.

        Returns:
            Callable[[~.DeleteGlossaryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_glossary" not in self._stubs:
            self._stubs["delete_glossary"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/DeleteGlossary",
                request_serializer=translation_service.DeleteGlossaryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_glossary"]

    @property
    def get_glossary_entry(
        self,
    ) -> Callable[
        [translation_service.GetGlossaryEntryRequest], Awaitable[common.GlossaryEntry]
    ]:
        r"""Return a callable for the get glossary entry method over gRPC.

        Gets a single glossary entry by the given id.

        Returns:
            Callable[[~.GetGlossaryEntryRequest],
                    Awaitable[~.GlossaryEntry]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_glossary_entry" not in self._stubs:
            self._stubs["get_glossary_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/GetGlossaryEntry",
                request_serializer=translation_service.GetGlossaryEntryRequest.serialize,
                response_deserializer=common.GlossaryEntry.deserialize,
            )
        return self._stubs["get_glossary_entry"]

    @property
    def list_glossary_entries(
        self,
    ) -> Callable[
        [translation_service.ListGlossaryEntriesRequest],
        Awaitable[translation_service.ListGlossaryEntriesResponse],
    ]:
        r"""Return a callable for the list glossary entries method over gRPC.

        List the entries for the glossary.

        Returns:
            Callable[[~.ListGlossaryEntriesRequest],
                    Awaitable[~.ListGlossaryEntriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_glossary_entries" not in self._stubs:
            self._stubs["list_glossary_entries"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListGlossaryEntries",
                request_serializer=translation_service.ListGlossaryEntriesRequest.serialize,
                response_deserializer=translation_service.ListGlossaryEntriesResponse.deserialize,
            )
        return self._stubs["list_glossary_entries"]

    @property
    def create_glossary_entry(
        self,
    ) -> Callable[
        [translation_service.CreateGlossaryEntryRequest],
        Awaitable[common.GlossaryEntry],
    ]:
        r"""Return a callable for the create glossary entry method over gRPC.

        Creates a glossary entry.

        Returns:
            Callable[[~.CreateGlossaryEntryRequest],
                    Awaitable[~.GlossaryEntry]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_glossary_entry" not in self._stubs:
            self._stubs["create_glossary_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/CreateGlossaryEntry",
                request_serializer=translation_service.CreateGlossaryEntryRequest.serialize,
                response_deserializer=common.GlossaryEntry.deserialize,
            )
        return self._stubs["create_glossary_entry"]

    @property
    def update_glossary_entry(
        self,
    ) -> Callable[
        [translation_service.UpdateGlossaryEntryRequest],
        Awaitable[common.GlossaryEntry],
    ]:
        r"""Return a callable for the update glossary entry method over gRPC.

        Updates a glossary entry.

        Returns:
            Callable[[~.UpdateGlossaryEntryRequest],
                    Awaitable[~.GlossaryEntry]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_glossary_entry" not in self._stubs:
            self._stubs["update_glossary_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/UpdateGlossaryEntry",
                request_serializer=translation_service.UpdateGlossaryEntryRequest.serialize,
                response_deserializer=common.GlossaryEntry.deserialize,
            )
        return self._stubs["update_glossary_entry"]

    @property
    def delete_glossary_entry(
        self,
    ) -> Callable[
        [translation_service.DeleteGlossaryEntryRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete glossary entry method over gRPC.

        Deletes a single entry from the glossary

        Returns:
            Callable[[~.DeleteGlossaryEntryRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_glossary_entry" not in self._stubs:
            self._stubs["delete_glossary_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/DeleteGlossaryEntry",
                request_serializer=translation_service.DeleteGlossaryEntryRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_glossary_entry"]

    @property
    def create_dataset(
        self,
    ) -> Callable[
        [automl_translation.CreateDatasetRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create dataset method over gRPC.

        Creates a Dataset.

        Returns:
            Callable[[~.CreateDatasetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_dataset" not in self._stubs:
            self._stubs["create_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/CreateDataset",
                request_serializer=automl_translation.CreateDatasetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_dataset"]

    @property
    def get_dataset(
        self,
    ) -> Callable[
        [automl_translation.GetDatasetRequest], Awaitable[automl_translation.Dataset]
    ]:
        r"""Return a callable for the get dataset method over gRPC.

        Gets a Dataset.

        Returns:
            Callable[[~.GetDatasetRequest],
                    Awaitable[~.Dataset]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_dataset" not in self._stubs:
            self._stubs["get_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/GetDataset",
                request_serializer=automl_translation.GetDatasetRequest.serialize,
                response_deserializer=automl_translation.Dataset.deserialize,
            )
        return self._stubs["get_dataset"]

    @property
    def list_datasets(
        self,
    ) -> Callable[
        [automl_translation.ListDatasetsRequest],
        Awaitable[automl_translation.ListDatasetsResponse],
    ]:
        r"""Return a callable for the list datasets method over gRPC.

        Lists datasets.

        Returns:
            Callable[[~.ListDatasetsRequest],
                    Awaitable[~.ListDatasetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_datasets" not in self._stubs:
            self._stubs["list_datasets"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListDatasets",
                request_serializer=automl_translation.ListDatasetsRequest.serialize,
                response_deserializer=automl_translation.ListDatasetsResponse.deserialize,
            )
        return self._stubs["list_datasets"]

    @property
    def delete_dataset(
        self,
    ) -> Callable[
        [automl_translation.DeleteDatasetRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete dataset method over gRPC.

        Deletes a dataset and all of its contents.

        Returns:
            Callable[[~.DeleteDatasetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_dataset" not in self._stubs:
            self._stubs["delete_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/DeleteDataset",
                request_serializer=automl_translation.DeleteDatasetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_dataset"]

    @property
    def create_adaptive_mt_dataset(
        self,
    ) -> Callable[
        [adaptive_mt.CreateAdaptiveMtDatasetRequest],
        Awaitable[adaptive_mt.AdaptiveMtDataset],
    ]:
        r"""Return a callable for the create adaptive mt dataset method over gRPC.

        Creates an Adaptive MT dataset.

        Returns:
            Callable[[~.CreateAdaptiveMtDatasetRequest],
                    Awaitable[~.AdaptiveMtDataset]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_adaptive_mt_dataset" not in self._stubs:
            self._stubs["create_adaptive_mt_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/CreateAdaptiveMtDataset",
                request_serializer=adaptive_mt.CreateAdaptiveMtDatasetRequest.serialize,
                response_deserializer=adaptive_mt.AdaptiveMtDataset.deserialize,
            )
        return self._stubs["create_adaptive_mt_dataset"]

    @property
    def delete_adaptive_mt_dataset(
        self,
    ) -> Callable[
        [adaptive_mt.DeleteAdaptiveMtDatasetRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete adaptive mt dataset method over gRPC.

        Deletes an Adaptive MT dataset, including all its
        entries and associated metadata.

        Returns:
            Callable[[~.DeleteAdaptiveMtDatasetRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_adaptive_mt_dataset" not in self._stubs:
            self._stubs["delete_adaptive_mt_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/DeleteAdaptiveMtDataset",
                request_serializer=adaptive_mt.DeleteAdaptiveMtDatasetRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_adaptive_mt_dataset"]

    @property
    def get_adaptive_mt_dataset(
        self,
    ) -> Callable[
        [adaptive_mt.GetAdaptiveMtDatasetRequest],
        Awaitable[adaptive_mt.AdaptiveMtDataset],
    ]:
        r"""Return a callable for the get adaptive mt dataset method over gRPC.

        Gets the Adaptive MT dataset.

        Returns:
            Callable[[~.GetAdaptiveMtDatasetRequest],
                    Awaitable[~.AdaptiveMtDataset]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_adaptive_mt_dataset" not in self._stubs:
            self._stubs["get_adaptive_mt_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/GetAdaptiveMtDataset",
                request_serializer=adaptive_mt.GetAdaptiveMtDatasetRequest.serialize,
                response_deserializer=adaptive_mt.AdaptiveMtDataset.deserialize,
            )
        return self._stubs["get_adaptive_mt_dataset"]

    @property
    def list_adaptive_mt_datasets(
        self,
    ) -> Callable[
        [adaptive_mt.ListAdaptiveMtDatasetsRequest],
        Awaitable[adaptive_mt.ListAdaptiveMtDatasetsResponse],
    ]:
        r"""Return a callable for the list adaptive mt datasets method over gRPC.

        Lists all Adaptive MT datasets for which the caller
        has read permission.

        Returns:
            Callable[[~.ListAdaptiveMtDatasetsRequest],
                    Awaitable[~.ListAdaptiveMtDatasetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_adaptive_mt_datasets" not in self._stubs:
            self._stubs["list_adaptive_mt_datasets"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListAdaptiveMtDatasets",
                request_serializer=adaptive_mt.ListAdaptiveMtDatasetsRequest.serialize,
                response_deserializer=adaptive_mt.ListAdaptiveMtDatasetsResponse.deserialize,
            )
        return self._stubs["list_adaptive_mt_datasets"]

    @property
    def adaptive_mt_translate(
        self,
    ) -> Callable[
        [adaptive_mt.AdaptiveMtTranslateRequest],
        Awaitable[adaptive_mt.AdaptiveMtTranslateResponse],
    ]:
        r"""Return a callable for the adaptive mt translate method over gRPC.

        Translate text using Adaptive MT.

        Returns:
            Callable[[~.AdaptiveMtTranslateRequest],
                    Awaitable[~.AdaptiveMtTranslateResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "adaptive_mt_translate" not in self._stubs:
            self._stubs["adaptive_mt_translate"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/AdaptiveMtTranslate",
                request_serializer=adaptive_mt.AdaptiveMtTranslateRequest.serialize,
                response_deserializer=adaptive_mt.AdaptiveMtTranslateResponse.deserialize,
            )
        return self._stubs["adaptive_mt_translate"]

    @property
    def get_adaptive_mt_file(
        self,
    ) -> Callable[
        [adaptive_mt.GetAdaptiveMtFileRequest], Awaitable[adaptive_mt.AdaptiveMtFile]
    ]:
        r"""Return a callable for the get adaptive mt file method over gRPC.

        Gets and AdaptiveMtFile

        Returns:
            Callable[[~.GetAdaptiveMtFileRequest],
                    Awaitable[~.AdaptiveMtFile]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_adaptive_mt_file" not in self._stubs:
            self._stubs["get_adaptive_mt_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/GetAdaptiveMtFile",
                request_serializer=adaptive_mt.GetAdaptiveMtFileRequest.serialize,
                response_deserializer=adaptive_mt.AdaptiveMtFile.deserialize,
            )
        return self._stubs["get_adaptive_mt_file"]

    @property
    def delete_adaptive_mt_file(
        self,
    ) -> Callable[
        [adaptive_mt.DeleteAdaptiveMtFileRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete adaptive mt file method over gRPC.

        Deletes an AdaptiveMtFile along with its sentences.

        Returns:
            Callable[[~.DeleteAdaptiveMtFileRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_adaptive_mt_file" not in self._stubs:
            self._stubs["delete_adaptive_mt_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/DeleteAdaptiveMtFile",
                request_serializer=adaptive_mt.DeleteAdaptiveMtFileRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_adaptive_mt_file"]

    @property
    def import_adaptive_mt_file(
        self,
    ) -> Callable[
        [adaptive_mt.ImportAdaptiveMtFileRequest],
        Awaitable[adaptive_mt.ImportAdaptiveMtFileResponse],
    ]:
        r"""Return a callable for the import adaptive mt file method over gRPC.

        Imports an AdaptiveMtFile and adds all of its
        sentences into the AdaptiveMtDataset.

        Returns:
            Callable[[~.ImportAdaptiveMtFileRequest],
                    Awaitable[~.ImportAdaptiveMtFileResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_adaptive_mt_file" not in self._stubs:
            self._stubs["import_adaptive_mt_file"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ImportAdaptiveMtFile",
                request_serializer=adaptive_mt.ImportAdaptiveMtFileRequest.serialize,
                response_deserializer=adaptive_mt.ImportAdaptiveMtFileResponse.deserialize,
            )
        return self._stubs["import_adaptive_mt_file"]

    @property
    def list_adaptive_mt_files(
        self,
    ) -> Callable[
        [adaptive_mt.ListAdaptiveMtFilesRequest],
        Awaitable[adaptive_mt.ListAdaptiveMtFilesResponse],
    ]:
        r"""Return a callable for the list adaptive mt files method over gRPC.

        Lists all AdaptiveMtFiles associated to an
        AdaptiveMtDataset.

        Returns:
            Callable[[~.ListAdaptiveMtFilesRequest],
                    Awaitable[~.ListAdaptiveMtFilesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_adaptive_mt_files" not in self._stubs:
            self._stubs["list_adaptive_mt_files"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListAdaptiveMtFiles",
                request_serializer=adaptive_mt.ListAdaptiveMtFilesRequest.serialize,
                response_deserializer=adaptive_mt.ListAdaptiveMtFilesResponse.deserialize,
            )
        return self._stubs["list_adaptive_mt_files"]

    @property
    def list_adaptive_mt_sentences(
        self,
    ) -> Callable[
        [adaptive_mt.ListAdaptiveMtSentencesRequest],
        Awaitable[adaptive_mt.ListAdaptiveMtSentencesResponse],
    ]:
        r"""Return a callable for the list adaptive mt sentences method over gRPC.

        Lists all AdaptiveMtSentences under a given
        file/dataset.

        Returns:
            Callable[[~.ListAdaptiveMtSentencesRequest],
                    Awaitable[~.ListAdaptiveMtSentencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_adaptive_mt_sentences" not in self._stubs:
            self._stubs["list_adaptive_mt_sentences"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListAdaptiveMtSentences",
                request_serializer=adaptive_mt.ListAdaptiveMtSentencesRequest.serialize,
                response_deserializer=adaptive_mt.ListAdaptiveMtSentencesResponse.deserialize,
            )
        return self._stubs["list_adaptive_mt_sentences"]

    @property
    def import_data(
        self,
    ) -> Callable[
        [automl_translation.ImportDataRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the import data method over gRPC.

        Import sentence pairs into translation Dataset.

        Returns:
            Callable[[~.ImportDataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_data" not in self._stubs:
            self._stubs["import_data"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ImportData",
                request_serializer=automl_translation.ImportDataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_data"]

    @property
    def export_data(
        self,
    ) -> Callable[
        [automl_translation.ExportDataRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the export data method over gRPC.

        Exports dataset's data to the provided output
        location.

        Returns:
            Callable[[~.ExportDataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_data" not in self._stubs:
            self._stubs["export_data"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ExportData",
                request_serializer=automl_translation.ExportDataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_data"]

    @property
    def list_examples(
        self,
    ) -> Callable[
        [automl_translation.ListExamplesRequest],
        Awaitable[automl_translation.ListExamplesResponse],
    ]:
        r"""Return a callable for the list examples method over gRPC.

        Lists sentence pairs in the dataset.

        Returns:
            Callable[[~.ListExamplesRequest],
                    Awaitable[~.ListExamplesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_examples" not in self._stubs:
            self._stubs["list_examples"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListExamples",
                request_serializer=automl_translation.ListExamplesRequest.serialize,
                response_deserializer=automl_translation.ListExamplesResponse.deserialize,
            )
        return self._stubs["list_examples"]

    @property
    def create_model(
        self,
    ) -> Callable[
        [automl_translation.CreateModelRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create model method over gRPC.

        Creates a Model.

        Returns:
            Callable[[~.CreateModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_model" not in self._stubs:
            self._stubs["create_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/CreateModel",
                request_serializer=automl_translation.CreateModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_model"]

    @property
    def list_models(
        self,
    ) -> Callable[
        [automl_translation.ListModelsRequest],
        Awaitable[automl_translation.ListModelsResponse],
    ]:
        r"""Return a callable for the list models method over gRPC.

        Lists models.

        Returns:
            Callable[[~.ListModelsRequest],
                    Awaitable[~.ListModelsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_models" not in self._stubs:
            self._stubs["list_models"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/ListModels",
                request_serializer=automl_translation.ListModelsRequest.serialize,
                response_deserializer=automl_translation.ListModelsResponse.deserialize,
            )
        return self._stubs["list_models"]

    @property
    def get_model(
        self,
    ) -> Callable[
        [automl_translation.GetModelRequest], Awaitable[automl_translation.Model]
    ]:
        r"""Return a callable for the get model method over gRPC.

        Gets a model.

        Returns:
            Callable[[~.GetModelRequest],
                    Awaitable[~.Model]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_model" not in self._stubs:
            self._stubs["get_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/GetModel",
                request_serializer=automl_translation.GetModelRequest.serialize,
                response_deserializer=automl_translation.Model.deserialize,
            )
        return self._stubs["get_model"]

    @property
    def delete_model(
        self,
    ) -> Callable[
        [automl_translation.DeleteModelRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete model method over gRPC.

        Deletes a model.

        Returns:
            Callable[[~.DeleteModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_model" not in self._stubs:
            self._stubs["delete_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.translation.v3.TranslationService/DeleteModel",
                request_serializer=automl_translation.DeleteModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_model"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.translate_text: self._wrap_method(
                self.translate_text,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.romanize_text: self._wrap_method(
                self.romanize_text,
                default_timeout=None,
                client_info=client_info,
            ),
            self.detect_language: self._wrap_method(
                self.detect_language,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.get_supported_languages: self._wrap_method(
                self.get_supported_languages,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.translate_document: self._wrap_method(
                self.translate_document,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.batch_translate_text: self._wrap_method(
                self.batch_translate_text,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.batch_translate_document: self._wrap_method(
                self.batch_translate_document,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.create_glossary: self._wrap_method(
                self.create_glossary,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.update_glossary: self._wrap_method(
                self.update_glossary,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_glossaries: self._wrap_method(
                self.list_glossaries,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.get_glossary: self._wrap_method(
                self.get_glossary,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.delete_glossary: self._wrap_method(
                self.delete_glossary,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.get_glossary_entry: self._wrap_method(
                self.get_glossary_entry,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_glossary_entries: self._wrap_method(
                self.list_glossary_entries,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_glossary_entry: self._wrap_method(
                self.create_glossary_entry,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_glossary_entry: self._wrap_method(
                self.update_glossary_entry,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_glossary_entry: self._wrap_method(
                self.delete_glossary_entry,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_dataset: self._wrap_method(
                self.create_dataset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_dataset: self._wrap_method(
                self.get_dataset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_datasets: self._wrap_method(
                self.list_datasets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_dataset: self._wrap_method(
                self.delete_dataset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_adaptive_mt_dataset: self._wrap_method(
                self.create_adaptive_mt_dataset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_adaptive_mt_dataset: self._wrap_method(
                self.delete_adaptive_mt_dataset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_adaptive_mt_dataset: self._wrap_method(
                self.get_adaptive_mt_dataset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_adaptive_mt_datasets: self._wrap_method(
                self.list_adaptive_mt_datasets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.adaptive_mt_translate: self._wrap_method(
                self.adaptive_mt_translate,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_adaptive_mt_file: self._wrap_method(
                self.get_adaptive_mt_file,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_adaptive_mt_file: self._wrap_method(
                self.delete_adaptive_mt_file,
                default_timeout=None,
                client_info=client_info,
            ),
            self.import_adaptive_mt_file: self._wrap_method(
                self.import_adaptive_mt_file,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_adaptive_mt_files: self._wrap_method(
                self.list_adaptive_mt_files,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_adaptive_mt_sentences: self._wrap_method(
                self.list_adaptive_mt_sentences,
                default_timeout=None,
                client_info=client_info,
            ),
            self.import_data: self._wrap_method(
                self.import_data,
                default_timeout=None,
                client_info=client_info,
            ),
            self.export_data: self._wrap_method(
                self.export_data,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_examples: self._wrap_method(
                self.list_examples,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_model: self._wrap_method(
                self.create_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_models: self._wrap_method(
                self.list_models,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_model: self._wrap_method(
                self.get_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_model: self._wrap_method(
                self.delete_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: self._wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: self._wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: self._wrap_method(
                self.list_operations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.wait_operation: self._wrap_method(
                self.wait_operation,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def wait_operation(
        self,
    ) -> Callable[[operations_pb2.WaitOperationRequest], None]:
        r"""Return a callable for the wait_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "wait_operation" not in self._stubs:
            self._stubs["wait_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/WaitOperation",
                request_serializer=operations_pb2.WaitOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["wait_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("TranslationServiceGrpcAsyncIOTransport",)
