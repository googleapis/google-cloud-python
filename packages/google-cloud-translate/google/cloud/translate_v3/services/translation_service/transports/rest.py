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
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.translate_v3.types import (
    adaptive_mt,
    automl_translation,
    common,
    translation_service,
)

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
            def pre_adaptive_mt_translate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_adaptive_mt_translate(self, response):
                logging.log(f"Received response: {response}")
                return response

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

            def pre_create_adaptive_mt_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_adaptive_mt_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_glossary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_glossary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_glossary_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_glossary_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_adaptive_mt_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_adaptive_mt_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_glossary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_glossary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_glossary_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_detect_language(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_detect_language(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_data(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_data(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_adaptive_mt_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_adaptive_mt_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_adaptive_mt_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_adaptive_mt_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_glossary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_glossary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_glossary_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_glossary_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_supported_languages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_supported_languages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_adaptive_mt_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_adaptive_mt_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_data(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_data(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_adaptive_mt_datasets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_adaptive_mt_datasets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_adaptive_mt_files(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_adaptive_mt_files(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_adaptive_mt_sentences(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_adaptive_mt_sentences(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_datasets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_datasets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_examples(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_examples(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_glossaries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_glossaries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_glossary_entries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_glossary_entries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_models(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_models(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_romanize_text(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_romanize_text(self, response):
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

            def pre_update_glossary(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_glossary(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_glossary_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_glossary_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = TranslationServiceRestTransport(interceptor=MyCustomTranslationServiceInterceptor())
        client = TranslationServiceClient(transport=transport)


    """

    def pre_adaptive_mt_translate(
        self,
        request: adaptive_mt.AdaptiveMtTranslateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.AdaptiveMtTranslateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for adaptive_mt_translate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_adaptive_mt_translate(
        self, response: adaptive_mt.AdaptiveMtTranslateResponse
    ) -> adaptive_mt.AdaptiveMtTranslateResponse:
        """Post-rpc interceptor for adaptive_mt_translate

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

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

    def pre_create_adaptive_mt_dataset(
        self,
        request: adaptive_mt.CreateAdaptiveMtDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.CreateAdaptiveMtDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_adaptive_mt_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_create_adaptive_mt_dataset(
        self, response: adaptive_mt.AdaptiveMtDataset
    ) -> adaptive_mt.AdaptiveMtDataset:
        """Post-rpc interceptor for create_adaptive_mt_dataset

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_create_dataset(
        self,
        request: automl_translation.CreateDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.CreateDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_create_dataset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_dataset

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

    def pre_create_glossary_entry(
        self,
        request: translation_service.CreateGlossaryEntryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        translation_service.CreateGlossaryEntryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_glossary_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_create_glossary_entry(
        self, response: common.GlossaryEntry
    ) -> common.GlossaryEntry:
        """Post-rpc interceptor for create_glossary_entry

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_create_model(
        self,
        request: automl_translation.CreateModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.CreateModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_create_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_model

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_adaptive_mt_dataset(
        self,
        request: adaptive_mt.DeleteAdaptiveMtDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.DeleteAdaptiveMtDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_adaptive_mt_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def pre_delete_adaptive_mt_file(
        self,
        request: adaptive_mt.DeleteAdaptiveMtFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.DeleteAdaptiveMtFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_adaptive_mt_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def pre_delete_dataset(
        self,
        request: automl_translation.DeleteDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.DeleteDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_delete_dataset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_dataset

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

    def pre_delete_glossary_entry(
        self,
        request: translation_service.DeleteGlossaryEntryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        translation_service.DeleteGlossaryEntryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_glossary_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def pre_delete_model(
        self,
        request: automl_translation.DeleteModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.DeleteModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_delete_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_model

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

    def pre_export_data(
        self,
        request: automl_translation.ExportDataRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.ExportDataRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_data

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_export_data(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_data

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_adaptive_mt_dataset(
        self,
        request: adaptive_mt.GetAdaptiveMtDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.GetAdaptiveMtDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_adaptive_mt_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_adaptive_mt_dataset(
        self, response: adaptive_mt.AdaptiveMtDataset
    ) -> adaptive_mt.AdaptiveMtDataset:
        """Post-rpc interceptor for get_adaptive_mt_dataset

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_adaptive_mt_file(
        self,
        request: adaptive_mt.GetAdaptiveMtFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.GetAdaptiveMtFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_adaptive_mt_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_adaptive_mt_file(
        self, response: adaptive_mt.AdaptiveMtFile
    ) -> adaptive_mt.AdaptiveMtFile:
        """Post-rpc interceptor for get_adaptive_mt_file

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_dataset(
        self,
        request: automl_translation.GetDatasetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.GetDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_dataset(
        self, response: automl_translation.Dataset
    ) -> automl_translation.Dataset:
        """Post-rpc interceptor for get_dataset

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

    def pre_get_glossary_entry(
        self,
        request: translation_service.GetGlossaryEntryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.GetGlossaryEntryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_glossary_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_glossary_entry(
        self, response: common.GlossaryEntry
    ) -> common.GlossaryEntry:
        """Post-rpc interceptor for get_glossary_entry

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_model(
        self,
        request: automl_translation.GetModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.GetModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_model(
        self, response: automl_translation.Model
    ) -> automl_translation.Model:
        """Post-rpc interceptor for get_model

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

    def pre_import_adaptive_mt_file(
        self,
        request: adaptive_mt.ImportAdaptiveMtFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.ImportAdaptiveMtFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_adaptive_mt_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_import_adaptive_mt_file(
        self, response: adaptive_mt.ImportAdaptiveMtFileResponse
    ) -> adaptive_mt.ImportAdaptiveMtFileResponse:
        """Post-rpc interceptor for import_adaptive_mt_file

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_import_data(
        self,
        request: automl_translation.ImportDataRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.ImportDataRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_data

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_import_data(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_data

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_adaptive_mt_datasets(
        self,
        request: adaptive_mt.ListAdaptiveMtDatasetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.ListAdaptiveMtDatasetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_adaptive_mt_datasets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_adaptive_mt_datasets(
        self, response: adaptive_mt.ListAdaptiveMtDatasetsResponse
    ) -> adaptive_mt.ListAdaptiveMtDatasetsResponse:
        """Post-rpc interceptor for list_adaptive_mt_datasets

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_adaptive_mt_files(
        self,
        request: adaptive_mt.ListAdaptiveMtFilesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.ListAdaptiveMtFilesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_adaptive_mt_files

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_adaptive_mt_files(
        self, response: adaptive_mt.ListAdaptiveMtFilesResponse
    ) -> adaptive_mt.ListAdaptiveMtFilesResponse:
        """Post-rpc interceptor for list_adaptive_mt_files

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_adaptive_mt_sentences(
        self,
        request: adaptive_mt.ListAdaptiveMtSentencesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[adaptive_mt.ListAdaptiveMtSentencesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_adaptive_mt_sentences

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_adaptive_mt_sentences(
        self, response: adaptive_mt.ListAdaptiveMtSentencesResponse
    ) -> adaptive_mt.ListAdaptiveMtSentencesResponse:
        """Post-rpc interceptor for list_adaptive_mt_sentences

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_datasets(
        self,
        request: automl_translation.ListDatasetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.ListDatasetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_datasets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_datasets(
        self, response: automl_translation.ListDatasetsResponse
    ) -> automl_translation.ListDatasetsResponse:
        """Post-rpc interceptor for list_datasets

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_examples(
        self,
        request: automl_translation.ListExamplesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.ListExamplesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_examples

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_examples(
        self, response: automl_translation.ListExamplesResponse
    ) -> automl_translation.ListExamplesResponse:
        """Post-rpc interceptor for list_examples

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

    def pre_list_glossary_entries(
        self,
        request: translation_service.ListGlossaryEntriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        translation_service.ListGlossaryEntriesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_glossary_entries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_glossary_entries(
        self, response: translation_service.ListGlossaryEntriesResponse
    ) -> translation_service.ListGlossaryEntriesResponse:
        """Post-rpc interceptor for list_glossary_entries

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_models(
        self,
        request: automl_translation.ListModelsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[automl_translation.ListModelsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_models

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_models(
        self, response: automl_translation.ListModelsResponse
    ) -> automl_translation.ListModelsResponse:
        """Post-rpc interceptor for list_models

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_romanize_text(
        self,
        request: translation_service.RomanizeTextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.RomanizeTextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for romanize_text

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_romanize_text(
        self, response: translation_service.RomanizeTextResponse
    ) -> translation_service.RomanizeTextResponse:
        """Post-rpc interceptor for romanize_text

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

    def pre_update_glossary(
        self,
        request: translation_service.UpdateGlossaryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[translation_service.UpdateGlossaryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_glossary

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_update_glossary(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_glossary

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_glossary_entry(
        self,
        request: translation_service.UpdateGlossaryEntryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        translation_service.UpdateGlossaryEntryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_glossary_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_update_glossary_entry(
        self, response: common.GlossaryEntry
    ) -> common.GlossaryEntry:
        """Post-rpc interceptor for update_glossary_entry

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
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
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
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
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
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
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the TranslationService server but before
        it is returned to user code.
        """
        return response

    def pre_wait_operation(
        self,
        request: operations_pb2.WaitOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.WaitOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for wait_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TranslationService server.
        """
        return request, metadata

    def post_wait_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for wait_operation

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
                 The hostname to connect to (default: 'translate.googleapis.com').
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
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v3/{name=projects/*/locations/*}/operations",
                    },
                ],
                "google.longrunning.Operations.WaitOperation": [
                    {
                        "method": "post",
                        "uri": "/v3/{name=projects/*/locations/*/operations/*}:wait",
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
                path_prefix="v3",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _AdaptiveMtTranslate(TranslationServiceRestStub):
        def __hash__(self):
            return hash("AdaptiveMtTranslate")

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
            request: adaptive_mt.AdaptiveMtTranslateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.AdaptiveMtTranslateResponse:
            r"""Call the adaptive mt translate method over HTTP.

            Args:
                request (~.adaptive_mt.AdaptiveMtTranslateRequest):
                    The request object. The request for sending an AdaptiveMt
                translation query.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.adaptive_mt.AdaptiveMtTranslateResponse:
                    An AdaptiveMtTranslate response.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*/locations/*}:adaptiveMtTranslate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_adaptive_mt_translate(
                request, metadata
            )
            pb_request = adaptive_mt.AdaptiveMtTranslateRequest.pb(request)
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
            resp = adaptive_mt.AdaptiveMtTranslateResponse()
            pb_resp = adaptive_mt.AdaptiveMtTranslateResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_adaptive_mt_translate(resp)
            return resp

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
                    "uri": "/v3/{parent=projects/*/locations/*}:batchTranslateDocument",
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
                    "uri": "/v3/{parent=projects/*/locations/*}:batchTranslateText",
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_translate_text(resp)
            return resp

    class _CreateAdaptiveMtDataset(TranslationServiceRestStub):
        def __hash__(self):
            return hash("CreateAdaptiveMtDataset")

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
            request: adaptive_mt.CreateAdaptiveMtDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.AdaptiveMtDataset:
            r"""Call the create adaptive mt
            dataset method over HTTP.

                Args:
                    request (~.adaptive_mt.CreateAdaptiveMtDatasetRequest):
                        The request object. Request message for creating an
                    AdaptiveMtDataset.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.adaptive_mt.AdaptiveMtDataset:
                        An Adaptive MT Dataset.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*/locations/*}/adaptiveMtDatasets",
                    "body": "adaptive_mt_dataset",
                },
            ]
            request, metadata = self._interceptor.pre_create_adaptive_mt_dataset(
                request, metadata
            )
            pb_request = adaptive_mt.CreateAdaptiveMtDatasetRequest.pb(request)
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
            resp = adaptive_mt.AdaptiveMtDataset()
            pb_resp = adaptive_mt.AdaptiveMtDataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_adaptive_mt_dataset(resp)
            return resp

    class _CreateDataset(TranslationServiceRestStub):
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
            request: automl_translation.CreateDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create dataset method over HTTP.

            Args:
                request (~.automl_translation.CreateDatasetRequest):
                    The request object. Request message for CreateDataset.
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
                    "uri": "/v3/{parent=projects/*/locations/*}/datasets",
                    "body": "dataset",
                },
            ]
            request, metadata = self._interceptor.pre_create_dataset(request, metadata)
            pb_request = automl_translation.CreateDatasetRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_dataset(resp)
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
                    "uri": "/v3/{parent=projects/*/locations/*}/glossaries",
                    "body": "glossary",
                },
            ]
            request, metadata = self._interceptor.pre_create_glossary(request, metadata)
            pb_request = translation_service.CreateGlossaryRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_glossary(resp)
            return resp

    class _CreateGlossaryEntry(TranslationServiceRestStub):
        def __hash__(self):
            return hash("CreateGlossaryEntry")

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
            request: translation_service.CreateGlossaryEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common.GlossaryEntry:
            r"""Call the create glossary entry method over HTTP.

            Args:
                request (~.translation_service.CreateGlossaryEntryRequest):
                    The request object. Request message for
                CreateGlossaryEntry
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common.GlossaryEntry:
                    Represents a single entry in a
                glossary.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*/locations/*/glossaries/*}/glossaryEntries",
                    "body": "glossary_entry",
                },
            ]
            request, metadata = self._interceptor.pre_create_glossary_entry(
                request, metadata
            )
            pb_request = translation_service.CreateGlossaryEntryRequest.pb(request)
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
            resp = common.GlossaryEntry()
            pb_resp = common.GlossaryEntry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_glossary_entry(resp)
            return resp

    class _CreateModel(TranslationServiceRestStub):
        def __hash__(self):
            return hash("CreateModel")

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
            request: automl_translation.CreateModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create model method over HTTP.

            Args:
                request (~.automl_translation.CreateModelRequest):
                    The request object. Request message for CreateModel.
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
                    "uri": "/v3/{parent=projects/*/locations/*}/models",
                    "body": "model",
                },
            ]
            request, metadata = self._interceptor.pre_create_model(request, metadata)
            pb_request = automl_translation.CreateModelRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_model(resp)
            return resp

    class _DeleteAdaptiveMtDataset(TranslationServiceRestStub):
        def __hash__(self):
            return hash("DeleteAdaptiveMtDataset")

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
            request: adaptive_mt.DeleteAdaptiveMtDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete adaptive mt
            dataset method over HTTP.

                Args:
                    request (~.adaptive_mt.DeleteAdaptiveMtDatasetRequest):
                        The request object. Request message for deleting an
                    AdaptiveMtDataset.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3/{name=projects/*/locations/*/adaptiveMtDatasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_adaptive_mt_dataset(
                request, metadata
            )
            pb_request = adaptive_mt.DeleteAdaptiveMtDatasetRequest.pb(request)
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

    class _DeleteAdaptiveMtFile(TranslationServiceRestStub):
        def __hash__(self):
            return hash("DeleteAdaptiveMtFile")

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
            request: adaptive_mt.DeleteAdaptiveMtFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete adaptive mt file method over HTTP.

            Args:
                request (~.adaptive_mt.DeleteAdaptiveMtFileRequest):
                    The request object. The request for deleting an
                AdaptiveMt file.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3/{name=projects/*/locations/*/adaptiveMtDatasets/*/adaptiveMtFiles/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_adaptive_mt_file(
                request, metadata
            )
            pb_request = adaptive_mt.DeleteAdaptiveMtFileRequest.pb(request)
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

    class _DeleteDataset(TranslationServiceRestStub):
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
            request: automl_translation.DeleteDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete dataset method over HTTP.

            Args:
                request (~.automl_translation.DeleteDatasetRequest):
                    The request object. Request message for DeleteDataset.
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
                    "uri": "/v3/{name=projects/*/locations/*/datasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_dataset(request, metadata)
            pb_request = automl_translation.DeleteDatasetRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_dataset(resp)
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
                    "uri": "/v3/{name=projects/*/locations/*/glossaries/*}",
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

    class _DeleteGlossaryEntry(TranslationServiceRestStub):
        def __hash__(self):
            return hash("DeleteGlossaryEntry")

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
            request: translation_service.DeleteGlossaryEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete glossary entry method over HTTP.

            Args:
                request (~.translation_service.DeleteGlossaryEntryRequest):
                    The request object. Request message for Delete Glossary
                Entry
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3/{name=projects/*/locations/*/glossaries/*/glossaryEntries/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_glossary_entry(
                request, metadata
            )
            pb_request = translation_service.DeleteGlossaryEntryRequest.pb(request)
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

    class _DeleteModel(TranslationServiceRestStub):
        def __hash__(self):
            return hash("DeleteModel")

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
            request: automl_translation.DeleteModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete model method over HTTP.

            Args:
                request (~.automl_translation.DeleteModelRequest):
                    The request object. Request message for DeleteModel.
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
                    "uri": "/v3/{name=projects/*/locations/*/models/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_model(request, metadata)
            pb_request = automl_translation.DeleteModelRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_model(resp)
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
                    "uri": "/v3/{parent=projects/*/locations/*}:detectLanguage",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*}:detectLanguage",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_detect_language(request, metadata)
            pb_request = translation_service.DetectLanguageRequest.pb(request)
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
            resp = translation_service.DetectLanguageResponse()
            pb_resp = translation_service.DetectLanguageResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_detect_language(resp)
            return resp

    class _ExportData(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ExportData")

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
            request: automl_translation.ExportDataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export data method over HTTP.

            Args:
                request (~.automl_translation.ExportDataRequest):
                    The request object. Request message for ExportData.
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
                    "uri": "/v3/{dataset=projects/*/locations/*/datasets/*}:exportData",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_export_data(request, metadata)
            pb_request = automl_translation.ExportDataRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_data(resp)
            return resp

    class _GetAdaptiveMtDataset(TranslationServiceRestStub):
        def __hash__(self):
            return hash("GetAdaptiveMtDataset")

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
            request: adaptive_mt.GetAdaptiveMtDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.AdaptiveMtDataset:
            r"""Call the get adaptive mt dataset method over HTTP.

            Args:
                request (~.adaptive_mt.GetAdaptiveMtDatasetRequest):
                    The request object. Request message for getting an
                Adaptive MT dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.adaptive_mt.AdaptiveMtDataset:
                    An Adaptive MT Dataset.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/adaptiveMtDatasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_adaptive_mt_dataset(
                request, metadata
            )
            pb_request = adaptive_mt.GetAdaptiveMtDatasetRequest.pb(request)
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
            resp = adaptive_mt.AdaptiveMtDataset()
            pb_resp = adaptive_mt.AdaptiveMtDataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_adaptive_mt_dataset(resp)
            return resp

    class _GetAdaptiveMtFile(TranslationServiceRestStub):
        def __hash__(self):
            return hash("GetAdaptiveMtFile")

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
            request: adaptive_mt.GetAdaptiveMtFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.AdaptiveMtFile:
            r"""Call the get adaptive mt file method over HTTP.

            Args:
                request (~.adaptive_mt.GetAdaptiveMtFileRequest):
                    The request object. The request for getting an
                AdaptiveMtFile.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.adaptive_mt.AdaptiveMtFile:
                    An AdaptiveMtFile.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/adaptiveMtDatasets/*/adaptiveMtFiles/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_adaptive_mt_file(
                request, metadata
            )
            pb_request = adaptive_mt.GetAdaptiveMtFileRequest.pb(request)
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
            resp = adaptive_mt.AdaptiveMtFile()
            pb_resp = adaptive_mt.AdaptiveMtFile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_adaptive_mt_file(resp)
            return resp

    class _GetDataset(TranslationServiceRestStub):
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
            request: automl_translation.GetDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> automl_translation.Dataset:
            r"""Call the get dataset method over HTTP.

            Args:
                request (~.automl_translation.GetDatasetRequest):
                    The request object. Request message for GetDataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.automl_translation.Dataset:
                    A dataset that hosts the examples
                (sentence pairs) used for translation
                models.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/datasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_dataset(request, metadata)
            pb_request = automl_translation.GetDatasetRequest.pb(request)
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
            resp = automl_translation.Dataset()
            pb_resp = automl_translation.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_dataset(resp)
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
                    Represents a glossary built from
                user-provided data.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/glossaries/*}",
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

    class _GetGlossaryEntry(TranslationServiceRestStub):
        def __hash__(self):
            return hash("GetGlossaryEntry")

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
            request: translation_service.GetGlossaryEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common.GlossaryEntry:
            r"""Call the get glossary entry method over HTTP.

            Args:
                request (~.translation_service.GetGlossaryEntryRequest):
                    The request object. Request message for the Get Glossary
                Entry Api
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common.GlossaryEntry:
                    Represents a single entry in a
                glossary.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/glossaries/*/glossaryEntries/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_glossary_entry(
                request, metadata
            )
            pb_request = translation_service.GetGlossaryEntryRequest.pb(request)
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
            resp = common.GlossaryEntry()
            pb_resp = common.GlossaryEntry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_glossary_entry(resp)
            return resp

    class _GetModel(TranslationServiceRestStub):
        def __hash__(self):
            return hash("GetModel")

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
            request: automl_translation.GetModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> automl_translation.Model:
            r"""Call the get model method over HTTP.

            Args:
                request (~.automl_translation.GetModelRequest):
                    The request object. Request message for GetModel.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.automl_translation.Model:
                    A trained translation model.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/models/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_model(request, metadata)
            pb_request = automl_translation.GetModelRequest.pb(request)
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
            resp = automl_translation.Model()
            pb_resp = automl_translation.Model.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_model(resp)
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
                    "uri": "/v3/{parent=projects/*/locations/*}/supportedLanguages",
                },
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*}/supportedLanguages",
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

    class _ImportAdaptiveMtFile(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ImportAdaptiveMtFile")

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
            request: adaptive_mt.ImportAdaptiveMtFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.ImportAdaptiveMtFileResponse:
            r"""Call the import adaptive mt file method over HTTP.

            Args:
                request (~.adaptive_mt.ImportAdaptiveMtFileRequest):
                    The request object. The request for importing an
                AdaptiveMt file along with its
                sentences.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.adaptive_mt.ImportAdaptiveMtFileResponse:
                    The response for importing an
                AdaptiveMtFile

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*/locations/*/adaptiveMtDatasets/*}:importAdaptiveMtFile",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_adaptive_mt_file(
                request, metadata
            )
            pb_request = adaptive_mt.ImportAdaptiveMtFileRequest.pb(request)
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
            resp = adaptive_mt.ImportAdaptiveMtFileResponse()
            pb_resp = adaptive_mt.ImportAdaptiveMtFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_adaptive_mt_file(resp)
            return resp

    class _ImportData(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ImportData")

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
            request: automl_translation.ImportDataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import data method over HTTP.

            Args:
                request (~.automl_translation.ImportDataRequest):
                    The request object. Request message for ImportData.
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
                    "uri": "/v3/{dataset=projects/*/locations/*/datasets/*}:importData",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_data(request, metadata)
            pb_request = automl_translation.ImportDataRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_data(resp)
            return resp

    class _ListAdaptiveMtDatasets(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ListAdaptiveMtDatasets")

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
            request: adaptive_mt.ListAdaptiveMtDatasetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.ListAdaptiveMtDatasetsResponse:
            r"""Call the list adaptive mt datasets method over HTTP.

            Args:
                request (~.adaptive_mt.ListAdaptiveMtDatasetsRequest):
                    The request object. Request message for listing all
                Adaptive MT datasets that the requestor
                has access to.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.adaptive_mt.ListAdaptiveMtDatasetsResponse:
                    A list of AdaptiveMtDatasets.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*}/adaptiveMtDatasets",
                },
            ]
            request, metadata = self._interceptor.pre_list_adaptive_mt_datasets(
                request, metadata
            )
            pb_request = adaptive_mt.ListAdaptiveMtDatasetsRequest.pb(request)
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
            resp = adaptive_mt.ListAdaptiveMtDatasetsResponse()
            pb_resp = adaptive_mt.ListAdaptiveMtDatasetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_adaptive_mt_datasets(resp)
            return resp

    class _ListAdaptiveMtFiles(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ListAdaptiveMtFiles")

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
            request: adaptive_mt.ListAdaptiveMtFilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.ListAdaptiveMtFilesResponse:
            r"""Call the list adaptive mt files method over HTTP.

            Args:
                request (~.adaptive_mt.ListAdaptiveMtFilesRequest):
                    The request object. The request to list all AdaptiveMt
                files under a given dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.adaptive_mt.ListAdaptiveMtFilesResponse:
                    The response for listing all
                AdaptiveMt files under a given dataset.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*/adaptiveMtDatasets/*}/adaptiveMtFiles",
                },
            ]
            request, metadata = self._interceptor.pre_list_adaptive_mt_files(
                request, metadata
            )
            pb_request = adaptive_mt.ListAdaptiveMtFilesRequest.pb(request)
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
            resp = adaptive_mt.ListAdaptiveMtFilesResponse()
            pb_resp = adaptive_mt.ListAdaptiveMtFilesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_adaptive_mt_files(resp)
            return resp

    class _ListAdaptiveMtSentences(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ListAdaptiveMtSentences")

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
            request: adaptive_mt.ListAdaptiveMtSentencesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> adaptive_mt.ListAdaptiveMtSentencesResponse:
            r"""Call the list adaptive mt
            sentences method over HTTP.

                Args:
                    request (~.adaptive_mt.ListAdaptiveMtSentencesRequest):
                        The request object. The request for listing Adaptive MT
                    sentences from a Dataset/File.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.adaptive_mt.ListAdaptiveMtSentencesResponse:
                        List AdaptiveMt sentences response.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*/adaptiveMtDatasets/*/adaptiveMtFiles/*}/adaptiveMtSentences",
                },
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*/adaptiveMtDatasets/*}/adaptiveMtSentences",
                },
            ]
            request, metadata = self._interceptor.pre_list_adaptive_mt_sentences(
                request, metadata
            )
            pb_request = adaptive_mt.ListAdaptiveMtSentencesRequest.pb(request)
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
            resp = adaptive_mt.ListAdaptiveMtSentencesResponse()
            pb_resp = adaptive_mt.ListAdaptiveMtSentencesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_adaptive_mt_sentences(resp)
            return resp

    class _ListDatasets(TranslationServiceRestStub):
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
            request: automl_translation.ListDatasetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> automl_translation.ListDatasetsResponse:
            r"""Call the list datasets method over HTTP.

            Args:
                request (~.automl_translation.ListDatasetsRequest):
                    The request object. Request message for ListDatasets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.automl_translation.ListDatasetsResponse:
                    Response message for ListDatasets.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*}/datasets",
                },
            ]
            request, metadata = self._interceptor.pre_list_datasets(request, metadata)
            pb_request = automl_translation.ListDatasetsRequest.pb(request)
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
            resp = automl_translation.ListDatasetsResponse()
            pb_resp = automl_translation.ListDatasetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_datasets(resp)
            return resp

    class _ListExamples(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ListExamples")

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
            request: automl_translation.ListExamplesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> automl_translation.ListExamplesResponse:
            r"""Call the list examples method over HTTP.

            Args:
                request (~.automl_translation.ListExamplesRequest):
                    The request object. Request message for ListExamples.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.automl_translation.ListExamplesResponse:
                    Response message for ListExamples.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*/datasets/*}/examples",
                },
            ]
            request, metadata = self._interceptor.pre_list_examples(request, metadata)
            pb_request = automl_translation.ListExamplesRequest.pb(request)
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
            resp = automl_translation.ListExamplesResponse()
            pb_resp = automl_translation.ListExamplesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_examples(resp)
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
                    "uri": "/v3/{parent=projects/*/locations/*}/glossaries",
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

    class _ListGlossaryEntries(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ListGlossaryEntries")

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
            request: translation_service.ListGlossaryEntriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.ListGlossaryEntriesResponse:
            r"""Call the list glossary entries method over HTTP.

            Args:
                request (~.translation_service.ListGlossaryEntriesRequest):
                    The request object. Request message for
                ListGlossaryEntries
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.ListGlossaryEntriesResponse:
                    Response message for
                ListGlossaryEntries

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*/glossaries/*}/glossaryEntries",
                },
            ]
            request, metadata = self._interceptor.pre_list_glossary_entries(
                request, metadata
            )
            pb_request = translation_service.ListGlossaryEntriesRequest.pb(request)
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
            resp = translation_service.ListGlossaryEntriesResponse()
            pb_resp = translation_service.ListGlossaryEntriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_glossary_entries(resp)
            return resp

    class _ListModels(TranslationServiceRestStub):
        def __hash__(self):
            return hash("ListModels")

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
            request: automl_translation.ListModelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> automl_translation.ListModelsResponse:
            r"""Call the list models method over HTTP.

            Args:
                request (~.automl_translation.ListModelsRequest):
                    The request object. Request message for ListModels.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.automl_translation.ListModelsResponse:
                    Response message for ListModels.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{parent=projects/*/locations/*}/models",
                },
            ]
            request, metadata = self._interceptor.pre_list_models(request, metadata)
            pb_request = automl_translation.ListModelsRequest.pb(request)
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
            resp = automl_translation.ListModelsResponse()
            pb_resp = automl_translation.ListModelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_models(resp)
            return resp

    class _RomanizeText(TranslationServiceRestStub):
        def __hash__(self):
            return hash("RomanizeText")

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
            request: translation_service.RomanizeTextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> translation_service.RomanizeTextResponse:
            r"""Call the romanize text method over HTTP.

            Args:
                request (~.translation_service.RomanizeTextRequest):
                    The request object. The request message for synchronous
                romanization.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.translation_service.RomanizeTextResponse:
                    The response message for synchronous
                romanization.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*/locations/*}:romanizeText",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*}:romanizeText",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_romanize_text(request, metadata)
            pb_request = translation_service.RomanizeTextRequest.pb(request)
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
            resp = translation_service.RomanizeTextResponse()
            pb_resp = translation_service.RomanizeTextResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_romanize_text(resp)
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
                    "uri": "/v3/{parent=projects/*/locations/*}:translateDocument",
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
                    "uri": "/v3/{parent=projects/*/locations/*}:translateText",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v3/{parent=projects/*}:translateText",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_translate_text(request, metadata)
            pb_request = translation_service.TranslateTextRequest.pb(request)
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
            resp = translation_service.TranslateTextResponse()
            pb_resp = translation_service.TranslateTextResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_translate_text(resp)
            return resp

    class _UpdateGlossary(TranslationServiceRestStub):
        def __hash__(self):
            return hash("UpdateGlossary")

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
            request: translation_service.UpdateGlossaryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update glossary method over HTTP.

            Args:
                request (~.translation_service.UpdateGlossaryRequest):
                    The request object. Request message for the update
                glossary flow
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
                    "method": "patch",
                    "uri": "/v3/{glossary.name=projects/*/locations/*/glossaries/*}",
                    "body": "glossary",
                },
            ]
            request, metadata = self._interceptor.pre_update_glossary(request, metadata)
            pb_request = translation_service.UpdateGlossaryRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_glossary(resp)
            return resp

    class _UpdateGlossaryEntry(TranslationServiceRestStub):
        def __hash__(self):
            return hash("UpdateGlossaryEntry")

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
            request: translation_service.UpdateGlossaryEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common.GlossaryEntry:
            r"""Call the update glossary entry method over HTTP.

            Args:
                request (~.translation_service.UpdateGlossaryEntryRequest):
                    The request object. Request message for
                UpdateGlossaryEntry
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common.GlossaryEntry:
                    Represents a single entry in a
                glossary.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v3/{glossary_entry.name=projects/*/locations/*/glossaries/*/glossaryEntries/*}",
                    "body": "glossary_entry",
                },
            ]
            request, metadata = self._interceptor.pre_update_glossary_entry(
                request, metadata
            )
            pb_request = translation_service.UpdateGlossaryEntryRequest.pb(request)
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
            resp = common.GlossaryEntry()
            pb_resp = common.GlossaryEntry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_glossary_entry(resp)
            return resp

    @property
    def adaptive_mt_translate(
        self,
    ) -> Callable[
        [adaptive_mt.AdaptiveMtTranslateRequest],
        adaptive_mt.AdaptiveMtTranslateResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AdaptiveMtTranslate(self._session, self._host, self._interceptor)  # type: ignore

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
    def create_adaptive_mt_dataset(
        self,
    ) -> Callable[
        [adaptive_mt.CreateAdaptiveMtDatasetRequest], adaptive_mt.AdaptiveMtDataset
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAdaptiveMtDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_dataset(
        self,
    ) -> Callable[[automl_translation.CreateDatasetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataset(self._session, self._host, self._interceptor)  # type: ignore

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
    def create_glossary_entry(
        self,
    ) -> Callable[
        [translation_service.CreateGlossaryEntryRequest], common.GlossaryEntry
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGlossaryEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_model(
        self,
    ) -> Callable[[automl_translation.CreateModelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_adaptive_mt_dataset(
        self,
    ) -> Callable[[adaptive_mt.DeleteAdaptiveMtDatasetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAdaptiveMtDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_adaptive_mt_file(
        self,
    ) -> Callable[[adaptive_mt.DeleteAdaptiveMtFileRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAdaptiveMtFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_dataset(
        self,
    ) -> Callable[[automl_translation.DeleteDatasetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataset(self._session, self._host, self._interceptor)  # type: ignore

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
    def delete_glossary_entry(
        self,
    ) -> Callable[[translation_service.DeleteGlossaryEntryRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGlossaryEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_model(
        self,
    ) -> Callable[[automl_translation.DeleteModelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteModel(self._session, self._host, self._interceptor)  # type: ignore

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
    def export_data(
        self,
    ) -> Callable[[automl_translation.ExportDataRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportData(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_adaptive_mt_dataset(
        self,
    ) -> Callable[
        [adaptive_mt.GetAdaptiveMtDatasetRequest], adaptive_mt.AdaptiveMtDataset
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAdaptiveMtDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_adaptive_mt_file(
        self,
    ) -> Callable[[adaptive_mt.GetAdaptiveMtFileRequest], adaptive_mt.AdaptiveMtFile]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAdaptiveMtFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_dataset(
        self,
    ) -> Callable[[automl_translation.GetDatasetRequest], automl_translation.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataset(self._session, self._host, self._interceptor)  # type: ignore

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
    def get_glossary_entry(
        self,
    ) -> Callable[[translation_service.GetGlossaryEntryRequest], common.GlossaryEntry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGlossaryEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_model(
        self,
    ) -> Callable[[automl_translation.GetModelRequest], automl_translation.Model]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetModel(self._session, self._host, self._interceptor)  # type: ignore

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
    def import_adaptive_mt_file(
        self,
    ) -> Callable[
        [adaptive_mt.ImportAdaptiveMtFileRequest],
        adaptive_mt.ImportAdaptiveMtFileResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportAdaptiveMtFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_data(
        self,
    ) -> Callable[[automl_translation.ImportDataRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportData(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_adaptive_mt_datasets(
        self,
    ) -> Callable[
        [adaptive_mt.ListAdaptiveMtDatasetsRequest],
        adaptive_mt.ListAdaptiveMtDatasetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAdaptiveMtDatasets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_adaptive_mt_files(
        self,
    ) -> Callable[
        [adaptive_mt.ListAdaptiveMtFilesRequest],
        adaptive_mt.ListAdaptiveMtFilesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAdaptiveMtFiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_adaptive_mt_sentences(
        self,
    ) -> Callable[
        [adaptive_mt.ListAdaptiveMtSentencesRequest],
        adaptive_mt.ListAdaptiveMtSentencesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAdaptiveMtSentences(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_datasets(
        self,
    ) -> Callable[
        [automl_translation.ListDatasetsRequest],
        automl_translation.ListDatasetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatasets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_examples(
        self,
    ) -> Callable[
        [automl_translation.ListExamplesRequest],
        automl_translation.ListExamplesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExamples(self._session, self._host, self._interceptor)  # type: ignore

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
    def list_glossary_entries(
        self,
    ) -> Callable[
        [translation_service.ListGlossaryEntriesRequest],
        translation_service.ListGlossaryEntriesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGlossaryEntries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_models(
        self,
    ) -> Callable[
        [automl_translation.ListModelsRequest], automl_translation.ListModelsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListModels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def romanize_text(
        self,
    ) -> Callable[
        [translation_service.RomanizeTextRequest],
        translation_service.RomanizeTextResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RomanizeText(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_glossary(
        self,
    ) -> Callable[
        [translation_service.UpdateGlossaryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGlossary(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_glossary_entry(
        self,
    ) -> Callable[
        [translation_service.UpdateGlossaryEntryRequest], common.GlossaryEntry
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGlossaryEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(TranslationServiceRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(TranslationServiceRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(TranslationServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(TranslationServiceRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v3/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(TranslationServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(TranslationServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v3/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def wait_operation(self):
        return self._WaitOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _WaitOperation(TranslationServiceRestStub):
        def __call__(
            self,
            request: operations_pb2.WaitOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the wait operation method over HTTP.

            Args:
                request (operations_pb2.WaitOperationRequest):
                    The request object for WaitOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from WaitOperation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v3/{name=projects/*/locations/*/operations/*}:wait",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_wait_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_wait_operation(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("TranslationServiceRestTransport",)
