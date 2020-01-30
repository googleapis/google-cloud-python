# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.cloud.translation.v3 TranslationService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.translate_v3.gapic import translation_service_client_config
from google.cloud.translate_v3.gapic.transports import (
    translation_service_grpc_transport,
)
from google.cloud.translate_v3.proto import translation_service_pb2
from google.cloud.translate_v3.proto import translation_service_pb2_grpc
from google.longrunning import operations_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-translate"
).version


class TranslationServiceClient(object):
    """Provides natural language translation operations."""

    SERVICE_ADDRESS = "translate.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.translation.v3.TranslationService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TranslationServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def glossary_path(cls, project, location, glossary):
        """Return a fully-qualified glossary string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/glossaries/{glossary}",
            project=project,
            location=location,
            glossary=glossary,
        )

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.TranslationServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.TranslationServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = translation_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=translation_service_grpc_transport.TranslationServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = translation_service_grpc_transport.TranslationServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def translate_text(
        self,
        contents,
        target_language_code,
        parent,
        mime_type=None,
        source_language_code=None,
        model=None,
        glossary_config=None,
        labels=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Translates input text and returns translated text.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> # TODO: Initialize `contents`:
            >>> contents = []
            >>>
            >>> # TODO: Initialize `target_language_code`:
            >>> target_language_code = ''
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> response = client.translate_text(contents, target_language_code, parent)

        Args:
            contents (list[str]): Required. The content of the input in string format.
                We recommend the total content be less than 30k codepoints.
                Use BatchTranslateText for larger text.
            target_language_code (str): Required. The BCP-47 language code to use for translation of the input
                text, set to one of the language codes listed in Language Support.
            parent (str): Required. Project or location to make a call. Must refer to a caller's
                project.

                Format: ``projects/{project-number-or-id}`` or
                ``projects/{project-number-or-id}/locations/{location-id}``.

                For global calls, use
                ``projects/{project-number-or-id}/locations/global`` or
                ``projects/{project-number-or-id}``.

                Non-global location is required for requests using AutoML models or
                custom glossaries.

                Models and glossaries must be within the same region (have same
                location-id), otherwise an INVALID\_ARGUMENT (400) error is returned.
            mime_type (str): Optional. The format of the source text, for example, "text/html",
                 "text/plain". If left blank, the MIME type defaults to "text/html".
            source_language_code (str): Optional. The BCP-47 language code of the input text if
                known, for example, "en-US" or "sr-Latn". Supported language codes are
                listed in Language Support. If the source language isn't specified, the API
                attempts to identify the source language automatically and returns the
                source language within the response.
            model (str): Optional. The ``model`` type requested for this translation.

                The format depends on model type:

                -  AutoML Translation models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/{model-id}``

                -  General (built-in) models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/nmt``,
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/base``

                For global (non-regionalized) requests, use ``location-id`` ``global``.
                For example,
                ``projects/{project-number-or-id}/locations/global/models/general/nmt``.

                If missing, the system decides which google base model to use.
            glossary_config (Union[dict, ~google.cloud.translate_v3.types.TranslateTextGlossaryConfig]): Optional. Glossary to be applied. The glossary must be within the same
                region (have the same location-id) as the model, otherwise an
                INVALID\_ARGUMENT (400) error is returned.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.translate_v3.types.TranslateTextGlossaryConfig`
            labels (dict[str -> str]): Optional. The labels with user-defined metadata for the request.

                Label keys and values can be no longer than 63 characters
                (Unicode codepoints), can only contain lowercase letters, numeric
                characters, underscores and dashes. International characters are allowed.
                Label values are optional. Label keys must start with a letter.

                See https://cloud.google.com/translate/docs/labels for more information.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.translate_v3.types.TranslateTextResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "translate_text" not in self._inner_api_calls:
            self._inner_api_calls[
                "translate_text"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.translate_text,
                default_retry=self._method_configs["TranslateText"].retry,
                default_timeout=self._method_configs["TranslateText"].timeout,
                client_info=self._client_info,
            )

        request = translation_service_pb2.TranslateTextRequest(
            contents=contents,
            target_language_code=target_language_code,
            parent=parent,
            mime_type=mime_type,
            source_language_code=source_language_code,
            model=model,
            glossary_config=glossary_config,
            labels=labels,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["translate_text"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def detect_language(
        self,
        parent,
        model=None,
        content=None,
        mime_type=None,
        labels=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Detects the language of text within a request.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> response = client.detect_language(parent)

        Args:
            parent (str): Required. Project or location to make a call. Must refer to a caller's
                project.

                Format: ``projects/{project-number-or-id}/locations/{location-id}`` or
                ``projects/{project-number-or-id}``.

                For global calls, use
                ``projects/{project-number-or-id}/locations/global`` or
                ``projects/{project-number-or-id}``.

                Only models within the same region (has same location-id) can be used.
                Otherwise an INVALID\_ARGUMENT (400) error is returned.
            model (str): Optional. The language detection model to be used.

                Format:
                ``projects/{project-number-or-id}/locations/{location-id}/models/language-detection/{model-id}``

                Only one language detection model is currently supported:
                ``projects/{project-number-or-id}/locations/{location-id}/models/language-detection/default``.

                If not specified, the default model is used.
            content (str): The content of the input stored as a string.
            mime_type (str): Optional. The format of the source text, for example, "text/html",
                "text/plain". If left blank, the MIME type defaults to "text/html".
            labels (dict[str -> str]): Optional. The labels with user-defined metadata for the request.

                Label keys and values can be no longer than 63 characters
                (Unicode codepoints), can only contain lowercase letters, numeric
                characters, underscores and dashes. International characters are allowed.
                Label values are optional. Label keys must start with a letter.

                See https://cloud.google.com/translate/docs/labels for more information.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.translate_v3.types.DetectLanguageResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "detect_language" not in self._inner_api_calls:
            self._inner_api_calls[
                "detect_language"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.detect_language,
                default_retry=self._method_configs["DetectLanguage"].retry,
                default_timeout=self._method_configs["DetectLanguage"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(content=content)

        request = translation_service_pb2.DetectLanguageRequest(
            parent=parent,
            model=model,
            content=content,
            mime_type=mime_type,
            labels=labels,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["detect_language"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_supported_languages(
        self,
        parent,
        display_language_code=None,
        model=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns a list of supported languages for translation.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> response = client.get_supported_languages(parent)

        Args:
            parent (str): Required. Project or location to make a call. Must refer to a caller's
                project.

                Format: ``projects/{project-number-or-id}`` or
                ``projects/{project-number-or-id}/locations/{location-id}``.

                For global calls, use
                ``projects/{project-number-or-id}/locations/global`` or
                ``projects/{project-number-or-id}``.

                Non-global location is required for AutoML models.

                Only models within the same region (have same location-id) can be used,
                otherwise an INVALID\_ARGUMENT (400) error is returned.
            display_language_code (str): Optional. The language to use to return localized, human readable names
                of supported languages. If missing, then display names are not returned
                in a response.
            model (str): Optional. Get supported languages of this model.

                The format depends on model type:

                -  AutoML Translation models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/{model-id}``

                -  General (built-in) models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/nmt``,
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/base``

                Returns languages supported by the specified model. If missing, we get
                supported languages of Google general base (PBMT) model.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.translate_v3.types.SupportedLanguages` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_supported_languages" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_supported_languages"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_supported_languages,
                default_retry=self._method_configs["GetSupportedLanguages"].retry,
                default_timeout=self._method_configs["GetSupportedLanguages"].timeout,
                client_info=self._client_info,
            )

        request = translation_service_pb2.GetSupportedLanguagesRequest(
            parent=parent, display_language_code=display_language_code, model=model
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_supported_languages"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_translate_text(
        self,
        parent,
        source_language_code,
        target_language_codes,
        input_configs,
        output_config,
        models=None,
        glossaries=None,
        labels=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Translates a large volume of text in asynchronous batch mode.
        This function provides real-time output as the inputs are being processed.
        If caller cancels a request, the partial results (for an input file, it's
        all or nothing) may still be available on the specified output location.

        This call returns immediately and you can
        use google.longrunning.Operation.name to poll the status of the call.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `source_language_code`:
            >>> source_language_code = ''
            >>>
            >>> # TODO: Initialize `target_language_codes`:
            >>> target_language_codes = []
            >>>
            >>> # TODO: Initialize `input_configs`:
            >>> input_configs = []
            >>>
            >>> # TODO: Initialize `output_config`:
            >>> output_config = {}
            >>>
            >>> response = client.batch_translate_text(parent, source_language_code, target_language_codes, input_configs, output_config)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. Location to make a call. Must refer to a caller's project.

                Format: ``projects/{project-number-or-id}/locations/{location-id}``.

                The ``global`` location is not supported for batch translation.

                Only AutoML Translation models or glossaries within the same region
                (have the same location-id) can be used, otherwise an INVALID\_ARGUMENT
                (400) error is returned.
            source_language_code (str): Required. Source language code.
            target_language_codes (list[str]): Required. Specify up to 10 language codes here.
            input_configs (list[Union[dict, ~google.cloud.translate_v3.types.InputConfig]]): Required. Input configurations.
                The total number of files matched should be <= 1000.
                The total content size should be <= 100M Unicode codepoints.
                The files must use UTF-8 encoding.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.translate_v3.types.InputConfig`
            output_config (Union[dict, ~google.cloud.translate_v3.types.OutputConfig]): Required. Output configuration.
                If 2 input configs match to the same file (that is, same input path),
                we don't generate output for duplicate inputs.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.translate_v3.types.OutputConfig`
            models (dict[str -> str]): Optional. The models to use for translation. Map's key is target
                language code. Map's value is model name. Value can be a built-in
                general model, or an AutoML Translation model.

                The value format depends on model type:

                -  AutoML Translation models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/{model-id}``

                -  General (built-in) models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/nmt``,
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/base``

                If the map is empty or a specific model is not requested for a language
                pair, then default google model (nmt) is used.
            glossaries (dict[str -> Union[dict, ~google.cloud.translate_v3.types.TranslateTextGlossaryConfig]]): Optional. Glossaries to be applied for translation.
                It's keyed by target language code.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.translate_v3.types.TranslateTextGlossaryConfig`
            labels (dict[str -> str]): Optional. The labels with user-defined metadata for the request.

                Label keys and values can be no longer than 63 characters
                (Unicode codepoints), can only contain lowercase letters, numeric
                characters, underscores and dashes. International characters are allowed.
                Label values are optional. Label keys must start with a letter.

                See https://cloud.google.com/translate/docs/labels for more information.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.translate_v3.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_translate_text" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_translate_text"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_translate_text,
                default_retry=self._method_configs["BatchTranslateText"].retry,
                default_timeout=self._method_configs["BatchTranslateText"].timeout,
                client_info=self._client_info,
            )

        request = translation_service_pb2.BatchTranslateTextRequest(
            parent=parent,
            source_language_code=source_language_code,
            target_language_codes=target_language_codes,
            input_configs=input_configs,
            output_config=output_config,
            models=models,
            glossaries=glossaries,
            labels=labels,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["batch_translate_text"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            translation_service_pb2.BatchTranslateResponse,
            metadata_type=translation_service_pb2.BatchTranslateMetadata,
        )

    def create_glossary(
        self,
        parent,
        glossary,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a glossary and returns the long-running operation. Returns
        NOT\_FOUND, if the project doesn't exist.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `glossary`:
            >>> glossary = {}
            >>>
            >>> response = client.create_glossary(parent, glossary)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The project name.
            glossary (Union[dict, ~google.cloud.translate_v3.types.Glossary]): Required. The glossary to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.translate_v3.types.Glossary`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.translate_v3.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_glossary" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_glossary"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_glossary,
                default_retry=self._method_configs["CreateGlossary"].retry,
                default_timeout=self._method_configs["CreateGlossary"].timeout,
                client_info=self._client_info,
            )

        request = translation_service_pb2.CreateGlossaryRequest(
            parent=parent, glossary=glossary
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["create_glossary"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            translation_service_pb2.Glossary,
            metadata_type=translation_service_pb2.CreateGlossaryMetadata,
        )

    def list_glossaries(
        self,
        parent,
        page_size=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists glossaries in a project. Returns NOT\_FOUND, if the project
        doesn't exist.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_glossaries(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_glossaries(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The name of the project from which to list all of the glossaries.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            filter_ (str): Optional. Filter specifying constraints of a list operation.
                Filtering is not supported yet, and the parameter currently has no effect.
                If missing, no filtering is performed.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.translate_v3.types.Glossary` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_glossaries" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_glossaries"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_glossaries,
                default_retry=self._method_configs["ListGlossaries"].retry,
                default_timeout=self._method_configs["ListGlossaries"].timeout,
                client_info=self._client_info,
            )

        request = translation_service_pb2.ListGlossariesRequest(
            parent=parent, page_size=page_size, filter=filter_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_glossaries"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="glossaries",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_glossary(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a glossary. Returns NOT\_FOUND, if the glossary doesn't exist.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> name = client.glossary_path('[PROJECT]', '[LOCATION]', '[GLOSSARY]')
            >>>
            >>> response = client.get_glossary(name)

        Args:
            name (str): Required. The name of the glossary to retrieve.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.translate_v3.types.Glossary` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_glossary" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_glossary"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_glossary,
                default_retry=self._method_configs["GetGlossary"].retry,
                default_timeout=self._method_configs["GetGlossary"].timeout,
                client_info=self._client_info,
            )

        request = translation_service_pb2.GetGlossaryRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_glossary"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_glossary(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a glossary, or cancels glossary construction if the glossary
        isn't created yet. Returns NOT\_FOUND, if the glossary doesn't exist.

        Example:
            >>> from google.cloud import translate_v3
            >>>
            >>> client = translate_v3.TranslationServiceClient()
            >>>
            >>> name = client.glossary_path('[PROJECT]', '[LOCATION]', '[GLOSSARY]')
            >>>
            >>> response = client.delete_glossary(name)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): Required. The name of the glossary to delete.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.translate_v3.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_glossary" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_glossary"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_glossary,
                default_retry=self._method_configs["DeleteGlossary"].retry,
                default_timeout=self._method_configs["DeleteGlossary"].timeout,
                client_info=self._client_info,
            )

        request = translation_service_pb2.DeleteGlossaryRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["delete_glossary"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            translation_service_pb2.DeleteGlossaryResponse,
            metadata_type=translation_service_pb2.DeleteGlossaryMetadata,
        )
