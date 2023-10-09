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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.api_core import operations_v1
from google.cloud.location import locations_pb2  # type: ignore
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.speech_v2.types import cloud_speech
from google.longrunning import operations_pb2  # type: ignore

from .base import SpeechTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class SpeechRestInterceptor:
    """Interceptor for Speech.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SpeechRestTransport.

    .. code-block:: python
        class MyCustomSpeechInterceptor(SpeechRestInterceptor):
            def pre_batch_recognize(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_recognize(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_custom_class(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_class(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_phrase_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_phrase_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_recognizer(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_recognizer(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_custom_class(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_custom_class(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_phrase_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_phrase_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_recognizer(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_recognizer(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_custom_class(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_class(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_phrase_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_phrase_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_recognizer(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_recognizer(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_custom_classes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_classes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_phrase_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_phrase_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_recognizers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_recognizers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_recognize(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_recognize(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_custom_class(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_custom_class(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_phrase_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_phrase_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_recognizer(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_recognizer(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_custom_class(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_custom_class(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_phrase_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_phrase_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_recognizer(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_recognizer(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SpeechRestTransport(interceptor=MyCustomSpeechInterceptor())
        client = SpeechClient(transport=transport)


    """

    def pre_batch_recognize(
        self,
        request: cloud_speech.BatchRecognizeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.BatchRecognizeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_recognize

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_batch_recognize(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_recognize

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_create_custom_class(
        self,
        request: cloud_speech.CreateCustomClassRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.CreateCustomClassRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_custom_class

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_create_custom_class(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_custom_class

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_create_phrase_set(
        self,
        request: cloud_speech.CreatePhraseSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.CreatePhraseSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_phrase_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_create_phrase_set(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_phrase_set

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_create_recognizer(
        self,
        request: cloud_speech.CreateRecognizerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.CreateRecognizerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_recognizer

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_create_recognizer(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_recognizer

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_delete_custom_class(
        self,
        request: cloud_speech.DeleteCustomClassRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.DeleteCustomClassRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_custom_class

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_delete_custom_class(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_custom_class

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_delete_phrase_set(
        self,
        request: cloud_speech.DeletePhraseSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.DeletePhraseSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_phrase_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_delete_phrase_set(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_phrase_set

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_delete_recognizer(
        self,
        request: cloud_speech.DeleteRecognizerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.DeleteRecognizerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_recognizer

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_delete_recognizer(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_recognizer

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_get_config(
        self,
        request: cloud_speech.GetConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.GetConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_get_config(self, response: cloud_speech.Config) -> cloud_speech.Config:
        """Post-rpc interceptor for get_config

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_get_custom_class(
        self,
        request: cloud_speech.GetCustomClassRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.GetCustomClassRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_custom_class

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_get_custom_class(
        self, response: cloud_speech.CustomClass
    ) -> cloud_speech.CustomClass:
        """Post-rpc interceptor for get_custom_class

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_get_phrase_set(
        self,
        request: cloud_speech.GetPhraseSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.GetPhraseSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_phrase_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_get_phrase_set(
        self, response: cloud_speech.PhraseSet
    ) -> cloud_speech.PhraseSet:
        """Post-rpc interceptor for get_phrase_set

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_get_recognizer(
        self,
        request: cloud_speech.GetRecognizerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.GetRecognizerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_recognizer

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_get_recognizer(
        self, response: cloud_speech.Recognizer
    ) -> cloud_speech.Recognizer:
        """Post-rpc interceptor for get_recognizer

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_list_custom_classes(
        self,
        request: cloud_speech.ListCustomClassesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.ListCustomClassesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_custom_classes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_list_custom_classes(
        self, response: cloud_speech.ListCustomClassesResponse
    ) -> cloud_speech.ListCustomClassesResponse:
        """Post-rpc interceptor for list_custom_classes

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_list_phrase_sets(
        self,
        request: cloud_speech.ListPhraseSetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.ListPhraseSetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_phrase_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_list_phrase_sets(
        self, response: cloud_speech.ListPhraseSetsResponse
    ) -> cloud_speech.ListPhraseSetsResponse:
        """Post-rpc interceptor for list_phrase_sets

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_list_recognizers(
        self,
        request: cloud_speech.ListRecognizersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.ListRecognizersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_recognizers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_list_recognizers(
        self, response: cloud_speech.ListRecognizersResponse
    ) -> cloud_speech.ListRecognizersResponse:
        """Post-rpc interceptor for list_recognizers

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_recognize(
        self,
        request: cloud_speech.RecognizeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.RecognizeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for recognize

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_recognize(
        self, response: cloud_speech.RecognizeResponse
    ) -> cloud_speech.RecognizeResponse:
        """Post-rpc interceptor for recognize

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_custom_class(
        self,
        request: cloud_speech.UndeleteCustomClassRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.UndeleteCustomClassRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_custom_class

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_undelete_custom_class(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_custom_class

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_phrase_set(
        self,
        request: cloud_speech.UndeletePhraseSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.UndeletePhraseSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_phrase_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_undelete_phrase_set(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_phrase_set

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_recognizer(
        self,
        request: cloud_speech.UndeleteRecognizerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.UndeleteRecognizerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_recognizer

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_undelete_recognizer(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_recognizer

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_update_config(
        self,
        request: cloud_speech.UpdateConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.UpdateConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_update_config(self, response: cloud_speech.Config) -> cloud_speech.Config:
        """Post-rpc interceptor for update_config

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_update_custom_class(
        self,
        request: cloud_speech.UpdateCustomClassRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.UpdateCustomClassRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_custom_class

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_update_custom_class(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_custom_class

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_update_phrase_set(
        self,
        request: cloud_speech.UpdatePhraseSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.UpdatePhraseSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_phrase_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_update_phrase_set(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_phrase_set

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response

    def pre_update_recognizer(
        self,
        request: cloud_speech.UpdateRecognizerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_speech.UpdateRecognizerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_recognizer

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_update_recognizer(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_recognizer

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
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
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
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
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
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
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
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
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
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
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
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
        before they are sent to the Speech server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Speech server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SpeechRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SpeechRestInterceptor


class SpeechRestTransport(SpeechTransport):
    """REST backend transport for Speech.

    Enables speech transcription and resource management.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "speech.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SpeechRestInterceptor] = None,
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
        self._interceptor = interceptor or SpeechRestInterceptor()
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
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchRecognize(SpeechRestStub):
        def __hash__(self):
            return hash("BatchRecognize")

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
            request: cloud_speech.BatchRecognizeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch recognize method over HTTP.

            Args:
                request (~.cloud_speech.BatchRecognizeRequest):
                    The request object. Request message for the
                [BatchRecognize][google.cloud.speech.v2.Speech.BatchRecognize]
                method.
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
                    "uri": "/v2/{recognizer=projects/*/locations/*/recognizers/*}:batchRecognize",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_recognize(request, metadata)
            pb_request = cloud_speech.BatchRecognizeRequest.pb(request)
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
            resp = self._interceptor.post_batch_recognize(resp)
            return resp

    class _CreateCustomClass(SpeechRestStub):
        def __hash__(self):
            return hash("CreateCustomClass")

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
            request: cloud_speech.CreateCustomClassRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create custom class method over HTTP.

            Args:
                request (~.cloud_speech.CreateCustomClassRequest):
                    The request object. Request message for the
                [CreateCustomClass][google.cloud.speech.v2.Speech.CreateCustomClass]
                method.
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
                    "uri": "/v2/{parent=projects/*/locations/*}/customClasses",
                    "body": "custom_class",
                },
            ]
            request, metadata = self._interceptor.pre_create_custom_class(
                request, metadata
            )
            pb_request = cloud_speech.CreateCustomClassRequest.pb(request)
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
            resp = self._interceptor.post_create_custom_class(resp)
            return resp

    class _CreatePhraseSet(SpeechRestStub):
        def __hash__(self):
            return hash("CreatePhraseSet")

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
            request: cloud_speech.CreatePhraseSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create phrase set method over HTTP.

            Args:
                request (~.cloud_speech.CreatePhraseSetRequest):
                    The request object. Request message for the
                [CreatePhraseSet][google.cloud.speech.v2.Speech.CreatePhraseSet]
                method.
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
                    "uri": "/v2/{parent=projects/*/locations/*}/phraseSets",
                    "body": "phrase_set",
                },
            ]
            request, metadata = self._interceptor.pre_create_phrase_set(
                request, metadata
            )
            pb_request = cloud_speech.CreatePhraseSetRequest.pb(request)
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
            resp = self._interceptor.post_create_phrase_set(resp)
            return resp

    class _CreateRecognizer(SpeechRestStub):
        def __hash__(self):
            return hash("CreateRecognizer")

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
            request: cloud_speech.CreateRecognizerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create recognizer method over HTTP.

            Args:
                request (~.cloud_speech.CreateRecognizerRequest):
                    The request object. Request message for the
                [CreateRecognizer][google.cloud.speech.v2.Speech.CreateRecognizer]
                method.
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
                    "uri": "/v2/{parent=projects/*/locations/*}/recognizers",
                    "body": "recognizer",
                },
            ]
            request, metadata = self._interceptor.pre_create_recognizer(
                request, metadata
            )
            pb_request = cloud_speech.CreateRecognizerRequest.pb(request)
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
            resp = self._interceptor.post_create_recognizer(resp)
            return resp

    class _DeleteCustomClass(SpeechRestStub):
        def __hash__(self):
            return hash("DeleteCustomClass")

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
            request: cloud_speech.DeleteCustomClassRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete custom class method over HTTP.

            Args:
                request (~.cloud_speech.DeleteCustomClassRequest):
                    The request object. Request message for the
                [DeleteCustomClass][google.cloud.speech.v2.Speech.DeleteCustomClass]
                method.
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
                    "uri": "/v2/{name=projects/*/locations/*/customClasses/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_custom_class(
                request, metadata
            )
            pb_request = cloud_speech.DeleteCustomClassRequest.pb(request)
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
            resp = self._interceptor.post_delete_custom_class(resp)
            return resp

    class _DeletePhraseSet(SpeechRestStub):
        def __hash__(self):
            return hash("DeletePhraseSet")

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
            request: cloud_speech.DeletePhraseSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete phrase set method over HTTP.

            Args:
                request (~.cloud_speech.DeletePhraseSetRequest):
                    The request object. Request message for the
                [DeletePhraseSet][google.cloud.speech.v2.Speech.DeletePhraseSet]
                method.
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
                    "uri": "/v2/{name=projects/*/locations/*/phraseSets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_phrase_set(
                request, metadata
            )
            pb_request = cloud_speech.DeletePhraseSetRequest.pb(request)
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
            resp = self._interceptor.post_delete_phrase_set(resp)
            return resp

    class _DeleteRecognizer(SpeechRestStub):
        def __hash__(self):
            return hash("DeleteRecognizer")

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
            request: cloud_speech.DeleteRecognizerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete recognizer method over HTTP.

            Args:
                request (~.cloud_speech.DeleteRecognizerRequest):
                    The request object. Request message for the
                [DeleteRecognizer][google.cloud.speech.v2.Speech.DeleteRecognizer]
                method.
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
                    "uri": "/v2/{name=projects/*/locations/*/recognizers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_recognizer(
                request, metadata
            )
            pb_request = cloud_speech.DeleteRecognizerRequest.pb(request)
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
            resp = self._interceptor.post_delete_recognizer(resp)
            return resp

    class _GetConfig(SpeechRestStub):
        def __hash__(self):
            return hash("GetConfig")

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
            request: cloud_speech.GetConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.Config:
            r"""Call the get config method over HTTP.

            Args:
                request (~.cloud_speech.GetConfigRequest):
                    The request object. Request message for the
                [GetConfig][google.cloud.speech.v2.Speech.GetConfig]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.Config:
                    Message representing the config for the Speech-to-Text
                API. This includes an optional `KMS
                key <https://cloud.google.com/kms/docs/resource-hierarchy#keys>`__
                with which incoming data will be encrypted.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/config}",
                },
            ]
            request, metadata = self._interceptor.pre_get_config(request, metadata)
            pb_request = cloud_speech.GetConfigRequest.pb(request)
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
            resp = cloud_speech.Config()
            pb_resp = cloud_speech.Config.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_config(resp)
            return resp

    class _GetCustomClass(SpeechRestStub):
        def __hash__(self):
            return hash("GetCustomClass")

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
            request: cloud_speech.GetCustomClassRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.CustomClass:
            r"""Call the get custom class method over HTTP.

            Args:
                request (~.cloud_speech.GetCustomClassRequest):
                    The request object. Request message for the
                [GetCustomClass][google.cloud.speech.v2.Speech.GetCustomClass]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.CustomClass:
                    CustomClass for biasing in speech
                recognition. Used to define a set of
                words or phrases that represents a
                common concept or theme likely to appear
                in your audio, for example a list of
                passenger ship names.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/customClasses/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_custom_class(
                request, metadata
            )
            pb_request = cloud_speech.GetCustomClassRequest.pb(request)
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
            resp = cloud_speech.CustomClass()
            pb_resp = cloud_speech.CustomClass.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_custom_class(resp)
            return resp

    class _GetPhraseSet(SpeechRestStub):
        def __hash__(self):
            return hash("GetPhraseSet")

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
            request: cloud_speech.GetPhraseSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.PhraseSet:
            r"""Call the get phrase set method over HTTP.

            Args:
                request (~.cloud_speech.GetPhraseSetRequest):
                    The request object. Request message for the
                [GetPhraseSet][google.cloud.speech.v2.Speech.GetPhraseSet]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.PhraseSet:
                    PhraseSet for biasing in speech
                recognition. A PhraseSet is used to
                provide "hints" to the speech recognizer
                to favor specific words and phrases in
                the results.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/phraseSets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_phrase_set(request, metadata)
            pb_request = cloud_speech.GetPhraseSetRequest.pb(request)
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
            resp = cloud_speech.PhraseSet()
            pb_resp = cloud_speech.PhraseSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_phrase_set(resp)
            return resp

    class _GetRecognizer(SpeechRestStub):
        def __hash__(self):
            return hash("GetRecognizer")

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
            request: cloud_speech.GetRecognizerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.Recognizer:
            r"""Call the get recognizer method over HTTP.

            Args:
                request (~.cloud_speech.GetRecognizerRequest):
                    The request object. Request message for the
                [GetRecognizer][google.cloud.speech.v2.Speech.GetRecognizer]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.Recognizer:
                    A Recognizer message. Stores
                recognition configuration and metadata.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/recognizers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_recognizer(request, metadata)
            pb_request = cloud_speech.GetRecognizerRequest.pb(request)
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
            resp = cloud_speech.Recognizer()
            pb_resp = cloud_speech.Recognizer.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_recognizer(resp)
            return resp

    class _ListCustomClasses(SpeechRestStub):
        def __hash__(self):
            return hash("ListCustomClasses")

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
            request: cloud_speech.ListCustomClassesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.ListCustomClassesResponse:
            r"""Call the list custom classes method over HTTP.

            Args:
                request (~.cloud_speech.ListCustomClassesRequest):
                    The request object. Request message for the
                [ListCustomClasses][google.cloud.speech.v2.Speech.ListCustomClasses]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.ListCustomClassesResponse:
                    Response message for the
                [ListCustomClasses][google.cloud.speech.v2.Speech.ListCustomClasses]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/customClasses",
                },
            ]
            request, metadata = self._interceptor.pre_list_custom_classes(
                request, metadata
            )
            pb_request = cloud_speech.ListCustomClassesRequest.pb(request)
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
            resp = cloud_speech.ListCustomClassesResponse()
            pb_resp = cloud_speech.ListCustomClassesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_custom_classes(resp)
            return resp

    class _ListPhraseSets(SpeechRestStub):
        def __hash__(self):
            return hash("ListPhraseSets")

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
            request: cloud_speech.ListPhraseSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.ListPhraseSetsResponse:
            r"""Call the list phrase sets method over HTTP.

            Args:
                request (~.cloud_speech.ListPhraseSetsRequest):
                    The request object. Request message for the
                [ListPhraseSets][google.cloud.speech.v2.Speech.ListPhraseSets]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.ListPhraseSetsResponse:
                    Response message for the
                [ListPhraseSets][google.cloud.speech.v2.Speech.ListPhraseSets]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/phraseSets",
                },
            ]
            request, metadata = self._interceptor.pre_list_phrase_sets(
                request, metadata
            )
            pb_request = cloud_speech.ListPhraseSetsRequest.pb(request)
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
            resp = cloud_speech.ListPhraseSetsResponse()
            pb_resp = cloud_speech.ListPhraseSetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_phrase_sets(resp)
            return resp

    class _ListRecognizers(SpeechRestStub):
        def __hash__(self):
            return hash("ListRecognizers")

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
            request: cloud_speech.ListRecognizersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.ListRecognizersResponse:
            r"""Call the list recognizers method over HTTP.

            Args:
                request (~.cloud_speech.ListRecognizersRequest):
                    The request object. Request message for the
                [ListRecognizers][google.cloud.speech.v2.Speech.ListRecognizers]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.ListRecognizersResponse:
                    Response message for the
                [ListRecognizers][google.cloud.speech.v2.Speech.ListRecognizers]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/recognizers",
                },
            ]
            request, metadata = self._interceptor.pre_list_recognizers(
                request, metadata
            )
            pb_request = cloud_speech.ListRecognizersRequest.pb(request)
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
            resp = cloud_speech.ListRecognizersResponse()
            pb_resp = cloud_speech.ListRecognizersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_recognizers(resp)
            return resp

    class _Recognize(SpeechRestStub):
        def __hash__(self):
            return hash("Recognize")

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
            request: cloud_speech.RecognizeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.RecognizeResponse:
            r"""Call the recognize method over HTTP.

            Args:
                request (~.cloud_speech.RecognizeRequest):
                    The request object. Request message for the
                [Recognize][google.cloud.speech.v2.Speech.Recognize]
                method. Either ``content`` or ``uri`` must be supplied.
                Supplying both or neither returns
                [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
                See `content
                limits <https://cloud.google.com/speech-to-text/quotas#content>`__.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.RecognizeResponse:
                    Response message for the
                [Recognize][google.cloud.speech.v2.Speech.Recognize]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{recognizer=projects/*/locations/*/recognizers/*}:recognize",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_recognize(request, metadata)
            pb_request = cloud_speech.RecognizeRequest.pb(request)
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
            resp = cloud_speech.RecognizeResponse()
            pb_resp = cloud_speech.RecognizeResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_recognize(resp)
            return resp

    class _StreamingRecognize(SpeechRestStub):
        def __hash__(self):
            return hash("StreamingRecognize")

        def __call__(
            self,
            request: cloud_speech.StreamingRecognizeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method StreamingRecognize is not available over REST transport"
            )

    class _UndeleteCustomClass(SpeechRestStub):
        def __hash__(self):
            return hash("UndeleteCustomClass")

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
            request: cloud_speech.UndeleteCustomClassRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete custom class method over HTTP.

            Args:
                request (~.cloud_speech.UndeleteCustomClassRequest):
                    The request object. Request message for the
                [UndeleteCustomClass][google.cloud.speech.v2.Speech.UndeleteCustomClass]
                method.
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
                    "uri": "/v2/{name=projects/*/locations/*/customClasses/*}:undelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undelete_custom_class(
                request, metadata
            )
            pb_request = cloud_speech.UndeleteCustomClassRequest.pb(request)
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
            resp = self._interceptor.post_undelete_custom_class(resp)
            return resp

    class _UndeletePhraseSet(SpeechRestStub):
        def __hash__(self):
            return hash("UndeletePhraseSet")

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
            request: cloud_speech.UndeletePhraseSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete phrase set method over HTTP.

            Args:
                request (~.cloud_speech.UndeletePhraseSetRequest):
                    The request object. Request message for the
                [UndeletePhraseSet][google.cloud.speech.v2.Speech.UndeletePhraseSet]
                method.
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
                    "uri": "/v2/{name=projects/*/locations/*/phraseSets/*}:undelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undelete_phrase_set(
                request, metadata
            )
            pb_request = cloud_speech.UndeletePhraseSetRequest.pb(request)
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
            resp = self._interceptor.post_undelete_phrase_set(resp)
            return resp

    class _UndeleteRecognizer(SpeechRestStub):
        def __hash__(self):
            return hash("UndeleteRecognizer")

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
            request: cloud_speech.UndeleteRecognizerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete recognizer method over HTTP.

            Args:
                request (~.cloud_speech.UndeleteRecognizerRequest):
                    The request object. Request message for the
                [UndeleteRecognizer][google.cloud.speech.v2.Speech.UndeleteRecognizer]
                method.
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
                    "uri": "/v2/{name=projects/*/locations/*/recognizers/*}:undelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undelete_recognizer(
                request, metadata
            )
            pb_request = cloud_speech.UndeleteRecognizerRequest.pb(request)
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
            resp = self._interceptor.post_undelete_recognizer(resp)
            return resp

    class _UpdateConfig(SpeechRestStub):
        def __hash__(self):
            return hash("UpdateConfig")

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
            request: cloud_speech.UpdateConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_speech.Config:
            r"""Call the update config method over HTTP.

            Args:
                request (~.cloud_speech.UpdateConfigRequest):
                    The request object. Request message for the
                [UpdateConfig][google.cloud.speech.v2.Speech.UpdateConfig]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_speech.Config:
                    Message representing the config for the Speech-to-Text
                API. This includes an optional `KMS
                key <https://cloud.google.com/kms/docs/resource-hierarchy#keys>`__
                with which incoming data will be encrypted.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{config.name=projects/*/locations/*/config}",
                    "body": "config",
                },
            ]
            request, metadata = self._interceptor.pre_update_config(request, metadata)
            pb_request = cloud_speech.UpdateConfigRequest.pb(request)
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
            resp = cloud_speech.Config()
            pb_resp = cloud_speech.Config.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_config(resp)
            return resp

    class _UpdateCustomClass(SpeechRestStub):
        def __hash__(self):
            return hash("UpdateCustomClass")

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
            request: cloud_speech.UpdateCustomClassRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update custom class method over HTTP.

            Args:
                request (~.cloud_speech.UpdateCustomClassRequest):
                    The request object. Request message for the
                [UpdateCustomClass][google.cloud.speech.v2.Speech.UpdateCustomClass]
                method.
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
                    "uri": "/v2/{custom_class.name=projects/*/locations/*/customClasses/*}",
                    "body": "custom_class",
                },
            ]
            request, metadata = self._interceptor.pre_update_custom_class(
                request, metadata
            )
            pb_request = cloud_speech.UpdateCustomClassRequest.pb(request)
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
            resp = self._interceptor.post_update_custom_class(resp)
            return resp

    class _UpdatePhraseSet(SpeechRestStub):
        def __hash__(self):
            return hash("UpdatePhraseSet")

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
            request: cloud_speech.UpdatePhraseSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update phrase set method over HTTP.

            Args:
                request (~.cloud_speech.UpdatePhraseSetRequest):
                    The request object. Request message for the
                [UpdatePhraseSet][google.cloud.speech.v2.Speech.UpdatePhraseSet]
                method.
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
                    "uri": "/v2/{phrase_set.name=projects/*/locations/*/phraseSets/*}",
                    "body": "phrase_set",
                },
            ]
            request, metadata = self._interceptor.pre_update_phrase_set(
                request, metadata
            )
            pb_request = cloud_speech.UpdatePhraseSetRequest.pb(request)
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
            resp = self._interceptor.post_update_phrase_set(resp)
            return resp

    class _UpdateRecognizer(SpeechRestStub):
        def __hash__(self):
            return hash("UpdateRecognizer")

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
            request: cloud_speech.UpdateRecognizerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update recognizer method over HTTP.

            Args:
                request (~.cloud_speech.UpdateRecognizerRequest):
                    The request object. Request message for the
                [UpdateRecognizer][google.cloud.speech.v2.Speech.UpdateRecognizer]
                method.
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
                    "uri": "/v2/{recognizer.name=projects/*/locations/*/recognizers/*}",
                    "body": "recognizer",
                },
            ]
            request, metadata = self._interceptor.pre_update_recognizer(
                request, metadata
            )
            pb_request = cloud_speech.UpdateRecognizerRequest.pb(request)
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
            resp = self._interceptor.post_update_recognizer(resp)
            return resp

    @property
    def batch_recognize(
        self,
    ) -> Callable[[cloud_speech.BatchRecognizeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchRecognize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_custom_class(
        self,
    ) -> Callable[[cloud_speech.CreateCustomClassRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCustomClass(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_phrase_set(
        self,
    ) -> Callable[[cloud_speech.CreatePhraseSetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePhraseSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_recognizer(
        self,
    ) -> Callable[[cloud_speech.CreateRecognizerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRecognizer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_custom_class(
        self,
    ) -> Callable[[cloud_speech.DeleteCustomClassRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCustomClass(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_phrase_set(
        self,
    ) -> Callable[[cloud_speech.DeletePhraseSetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePhraseSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_recognizer(
        self,
    ) -> Callable[[cloud_speech.DeleteRecognizerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRecognizer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_config(
        self,
    ) -> Callable[[cloud_speech.GetConfigRequest], cloud_speech.Config]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_custom_class(
        self,
    ) -> Callable[[cloud_speech.GetCustomClassRequest], cloud_speech.CustomClass]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomClass(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_phrase_set(
        self,
    ) -> Callable[[cloud_speech.GetPhraseSetRequest], cloud_speech.PhraseSet]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPhraseSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_recognizer(
        self,
    ) -> Callable[[cloud_speech.GetRecognizerRequest], cloud_speech.Recognizer]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRecognizer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_custom_classes(
        self,
    ) -> Callable[
        [cloud_speech.ListCustomClassesRequest], cloud_speech.ListCustomClassesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomClasses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_phrase_sets(
        self,
    ) -> Callable[
        [cloud_speech.ListPhraseSetsRequest], cloud_speech.ListPhraseSetsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPhraseSets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_recognizers(
        self,
    ) -> Callable[
        [cloud_speech.ListRecognizersRequest], cloud_speech.ListRecognizersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRecognizers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def recognize(
        self,
    ) -> Callable[[cloud_speech.RecognizeRequest], cloud_speech.RecognizeResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Recognize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def streaming_recognize(
        self,
    ) -> Callable[
        [cloud_speech.StreamingRecognizeRequest],
        cloud_speech.StreamingRecognizeResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StreamingRecognize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_custom_class(
        self,
    ) -> Callable[[cloud_speech.UndeleteCustomClassRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteCustomClass(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_phrase_set(
        self,
    ) -> Callable[[cloud_speech.UndeletePhraseSetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeletePhraseSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_recognizer(
        self,
    ) -> Callable[[cloud_speech.UndeleteRecognizerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteRecognizer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_config(
        self,
    ) -> Callable[[cloud_speech.UpdateConfigRequest], cloud_speech.Config]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_custom_class(
        self,
    ) -> Callable[[cloud_speech.UpdateCustomClassRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCustomClass(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_phrase_set(
        self,
    ) -> Callable[[cloud_speech.UpdatePhraseSetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePhraseSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_recognizer(
        self,
    ) -> Callable[[cloud_speech.UpdateRecognizerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRecognizer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(SpeechRestStub):
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
                    "uri": "/v2/{name=projects/*/locations/*}",
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

    class _ListLocations(SpeechRestStub):
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
                    "uri": "/v2/{name=projects/*}/locations",
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

    class _CancelOperation(SpeechRestStub):
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
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}:cancel",
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

    class _DeleteOperation(SpeechRestStub):
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
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}",
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

    class _GetOperation(SpeechRestStub):
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
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(SpeechRestStub):
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
                    "uri": "/v2/{name=projects/*/locations/*}/operations",
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SpeechRestTransport",)
