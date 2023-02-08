# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
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
from google.longrunning import operations_pb2
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.documentai_v1beta3.types import document_processor_service, evaluation
from google.cloud.documentai_v1beta3.types import processor
from google.cloud.documentai_v1beta3.types import processor as gcd_processor
from google.cloud.documentai_v1beta3.types import processor_type

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DocumentProcessorServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class DocumentProcessorServiceRestInterceptor:
    """Interceptor for DocumentProcessorService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DocumentProcessorServiceRestTransport.

    .. code-block:: python
        class MyCustomDocumentProcessorServiceInterceptor(DocumentProcessorServiceRestInterceptor):
            def pre_batch_process_documents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_process_documents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_processor_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_processor_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_deploy_processor_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_deploy_processor_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_evaluate_processor_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_evaluate_processor_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_processor_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_processor_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_evaluation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_evaluation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_processor(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_processor(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_processor_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_processor_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_processor_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_processor_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_evaluations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_evaluations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_processors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_processors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_processor_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_processor_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_processor_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_processor_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_process_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_process_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_review_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_review_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_default_processor_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_default_processor_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_train_processor_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_train_processor_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undeploy_processor_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undeploy_processor_version(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DocumentProcessorServiceRestTransport(interceptor=MyCustomDocumentProcessorServiceInterceptor())
        client = DocumentProcessorServiceClient(transport=transport)


    """

    def pre_batch_process_documents(
        self,
        request: document_processor_service.BatchProcessRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.BatchProcessRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_process_documents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_batch_process_documents(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_process_documents

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_create_processor(
        self,
        request: document_processor_service.CreateProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.CreateProcessorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_create_processor(
        self, response: gcd_processor.Processor
    ) -> gcd_processor.Processor:
        """Post-rpc interceptor for create_processor

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_processor(
        self,
        request: document_processor_service.DeleteProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.DeleteProcessorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_delete_processor(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_processor

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_processor_version(
        self,
        request: document_processor_service.DeleteProcessorVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.DeleteProcessorVersionRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_processor_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_delete_processor_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_processor_version

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_deploy_processor_version(
        self,
        request: document_processor_service.DeployProcessorVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.DeployProcessorVersionRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for deploy_processor_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_deploy_processor_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for deploy_processor_version

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_disable_processor(
        self,
        request: document_processor_service.DisableProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.DisableProcessorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for disable_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_disable_processor(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for disable_processor

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_enable_processor(
        self,
        request: document_processor_service.EnableProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.EnableProcessorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for enable_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_enable_processor(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for enable_processor

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_evaluate_processor_version(
        self,
        request: document_processor_service.EvaluateProcessorVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.EvaluateProcessorVersionRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for evaluate_processor_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_evaluate_processor_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for evaluate_processor_version

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_processor_types(
        self,
        request: document_processor_service.FetchProcessorTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.FetchProcessorTypesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for fetch_processor_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_fetch_processor_types(
        self, response: document_processor_service.FetchProcessorTypesResponse
    ) -> document_processor_service.FetchProcessorTypesResponse:
        """Post-rpc interceptor for fetch_processor_types

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_get_evaluation(
        self,
        request: document_processor_service.GetEvaluationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.GetEvaluationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_evaluation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_get_evaluation(
        self, response: evaluation.Evaluation
    ) -> evaluation.Evaluation:
        """Post-rpc interceptor for get_evaluation

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_get_processor(
        self,
        request: document_processor_service.GetProcessorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.GetProcessorRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_processor

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_get_processor(self, response: processor.Processor) -> processor.Processor:
        """Post-rpc interceptor for get_processor

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_get_processor_type(
        self,
        request: document_processor_service.GetProcessorTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.GetProcessorTypeRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_processor_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_get_processor_type(
        self, response: processor_type.ProcessorType
    ) -> processor_type.ProcessorType:
        """Post-rpc interceptor for get_processor_type

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_get_processor_version(
        self,
        request: document_processor_service.GetProcessorVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.GetProcessorVersionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_processor_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_get_processor_version(
        self, response: processor.ProcessorVersion
    ) -> processor.ProcessorVersion:
        """Post-rpc interceptor for get_processor_version

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_list_evaluations(
        self,
        request: document_processor_service.ListEvaluationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.ListEvaluationsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_evaluations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_list_evaluations(
        self, response: document_processor_service.ListEvaluationsResponse
    ) -> document_processor_service.ListEvaluationsResponse:
        """Post-rpc interceptor for list_evaluations

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_list_processors(
        self,
        request: document_processor_service.ListProcessorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.ListProcessorsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_processors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_list_processors(
        self, response: document_processor_service.ListProcessorsResponse
    ) -> document_processor_service.ListProcessorsResponse:
        """Post-rpc interceptor for list_processors

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_list_processor_types(
        self,
        request: document_processor_service.ListProcessorTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.ListProcessorTypesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_processor_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_list_processor_types(
        self, response: document_processor_service.ListProcessorTypesResponse
    ) -> document_processor_service.ListProcessorTypesResponse:
        """Post-rpc interceptor for list_processor_types

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_list_processor_versions(
        self,
        request: document_processor_service.ListProcessorVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.ListProcessorVersionsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_processor_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_list_processor_versions(
        self, response: document_processor_service.ListProcessorVersionsResponse
    ) -> document_processor_service.ListProcessorVersionsResponse:
        """Post-rpc interceptor for list_processor_versions

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_process_document(
        self,
        request: document_processor_service.ProcessRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[document_processor_service.ProcessRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for process_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_process_document(
        self, response: document_processor_service.ProcessResponse
    ) -> document_processor_service.ProcessResponse:
        """Post-rpc interceptor for process_document

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_review_document(
        self,
        request: document_processor_service.ReviewDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.ReviewDocumentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for review_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_review_document(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for review_document

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_set_default_processor_version(
        self,
        request: document_processor_service.SetDefaultProcessorVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.SetDefaultProcessorVersionRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for set_default_processor_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_set_default_processor_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for set_default_processor_version

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_train_processor_version(
        self,
        request: document_processor_service.TrainProcessorVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.TrainProcessorVersionRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for train_processor_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_train_processor_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for train_processor_version

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_undeploy_processor_version(
        self,
        request: document_processor_service.UndeployProcessorVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_processor_service.UndeployProcessorVersionRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for undeploy_processor_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_undeploy_processor_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undeploy_processor_version

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> locations_pb2.Location:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.GetLocationRequest
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> locations_pb2.ListLocationsResponse:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsRequest
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> None:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_cancel_operation(
        self, response: operations_pb2.CancelOperationRequest
    ) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> operations_pb2.Operation:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.GetOperationRequest
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> operations_pb2.ListOperationsResponse:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentProcessorService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsRequest
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the DocumentProcessorService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DocumentProcessorServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DocumentProcessorServiceRestInterceptor


class DocumentProcessorServiceRestTransport(DocumentProcessorServiceTransport):
    """REST backend transport for DocumentProcessorService.

    Service to call Cloud DocumentAI to process documents
    according to the processor's definition. Processors are built
    using state-of-the-art Google AI such as natural language,
    computer vision, and translation to extract structured
    information from unstructured or semi-structured documents.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "documentai.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DocumentProcessorServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or DocumentProcessorServiceRestInterceptor()
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
                        "uri": "/v1beta3/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                    {
                        "method": "post",
                        "uri": "/uiv1beta3/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta3/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/uiv1beta3/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta3/{name=projects/*/locations/*/operations}",
                    },
                    {
                        "method": "get",
                        "uri": "/uiv1beta3/{name=projects/*/locations/*/operations}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta3",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchProcessDocuments(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("BatchProcessDocuments")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.BatchProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch process documents method over HTTP.

            Args:
                request (~.document_processor_service.BatchProcessRequest):
                    The request object. Request message for batch process
                document method.

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
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*}:batchProcess",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*/processorVersions/*}:batchProcess",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_process_documents(
                request, metadata
            )
            pb_request = document_processor_service.BatchProcessRequest.pb(request)
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
            resp = self._interceptor.post_batch_process_documents(resp)
            return resp

    class _CreateProcessor(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("CreateProcessor")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.CreateProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_processor.Processor:
            r"""Call the create processor method over HTTP.

            Args:
                request (~.document_processor_service.CreateProcessorRequest):
                    The request object. Request message for create a
                processor. Notice this request is sent
                to a regionalized backend service, and
                if the processor type is not available
                on that region, the creation will fail.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_processor.Processor:
                    The first-class citizen for Document
                AI. Each processor defines how to
                extract structural information from a
                document.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta3/{parent=projects/*/locations/*}/processors",
                    "body": "processor",
                },
            ]
            request, metadata = self._interceptor.pre_create_processor(
                request, metadata
            )
            pb_request = document_processor_service.CreateProcessorRequest.pb(request)
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
            resp = gcd_processor.Processor()
            pb_resp = gcd_processor.Processor.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_processor(resp)
            return resp

    class _DeleteProcessor(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("DeleteProcessor")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.DeleteProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete processor method over HTTP.

            Args:
                request (~.document_processor_service.DeleteProcessorRequest):
                    The request object. Request message for the delete
                processor method.

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
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_processor(
                request, metadata
            )
            pb_request = document_processor_service.DeleteProcessorRequest.pb(request)
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
            resp = self._interceptor.post_delete_processor(resp)
            return resp

    class _DeleteProcessorVersion(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("DeleteProcessorVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.DeleteProcessorVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete processor version method over HTTP.

            Args:
                request (~.document_processor_service.DeleteProcessorVersionRequest):
                    The request object. Request message for the delete
                processor version method.

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
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*/processorVersions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_processor_version(
                request, metadata
            )
            pb_request = document_processor_service.DeleteProcessorVersionRequest.pb(
                request
            )
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
            resp = self._interceptor.post_delete_processor_version(resp)
            return resp

    class _DeployProcessorVersion(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("DeployProcessorVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.DeployProcessorVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the deploy processor version method over HTTP.

            Args:
                request (~.document_processor_service.DeployProcessorVersionRequest):
                    The request object. Request message for the deploy
                processor version method.

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
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*/processorVersions/*}:deploy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_deploy_processor_version(
                request, metadata
            )
            pb_request = document_processor_service.DeployProcessorVersionRequest.pb(
                request
            )
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
            resp = self._interceptor.post_deploy_processor_version(resp)
            return resp

    class _DisableProcessor(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("DisableProcessor")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.DisableProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the disable processor method over HTTP.

            Args:
                request (~.document_processor_service.DisableProcessorRequest):
                    The request object. Request message for the disable
                processor method.

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
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*}:disable",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_disable_processor(
                request, metadata
            )
            pb_request = document_processor_service.DisableProcessorRequest.pb(request)
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
            resp = self._interceptor.post_disable_processor(resp)
            return resp

    class _EnableProcessor(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("EnableProcessor")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.EnableProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the enable processor method over HTTP.

            Args:
                request (~.document_processor_service.EnableProcessorRequest):
                    The request object. Request message for the enable
                processor method.

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
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*}:enable",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_enable_processor(
                request, metadata
            )
            pb_request = document_processor_service.EnableProcessorRequest.pb(request)
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
            resp = self._interceptor.post_enable_processor(resp)
            return resp

    class _EvaluateProcessorVersion(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("EvaluateProcessorVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.EvaluateProcessorVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the evaluate processor
            version method over HTTP.

                Args:
                    request (~.document_processor_service.EvaluateProcessorVersionRequest):
                        The request object. Evaluates the given ProcessorVersion
                    against the supplied documents.

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
                    "uri": "/v1beta3/{processor_version=projects/*/locations/*/processors/*/processorVersions/*}:evaluateProcessorVersion",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_evaluate_processor_version(
                request, metadata
            )
            pb_request = document_processor_service.EvaluateProcessorVersionRequest.pb(
                request
            )
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
            resp = self._interceptor.post_evaluate_processor_version(resp)
            return resp

    class _FetchProcessorTypes(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("FetchProcessorTypes")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.FetchProcessorTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_processor_service.FetchProcessorTypesResponse:
            r"""Call the fetch processor types method over HTTP.

            Args:
                request (~.document_processor_service.FetchProcessorTypesRequest):
                    The request object. Request message for fetch processor
                types.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_processor_service.FetchProcessorTypesResponse:
                    Response message for fetch processor
                types.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{parent=projects/*/locations/*}:fetchProcessorTypes",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_processor_types(
                request, metadata
            )
            pb_request = document_processor_service.FetchProcessorTypesRequest.pb(
                request
            )
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
            resp = document_processor_service.FetchProcessorTypesResponse()
            pb_resp = document_processor_service.FetchProcessorTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_processor_types(resp)
            return resp

    class _GetEvaluation(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("GetEvaluation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.GetEvaluationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> evaluation.Evaluation:
            r"""Call the get evaluation method over HTTP.

            Args:
                request (~.document_processor_service.GetEvaluationRequest):
                    The request object. Retrieves a specific Evaluation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.evaluation.Evaluation:
                    An evaluation of a ProcessorVersion's
                performance.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*/processorVersions/*/evaluations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_evaluation(request, metadata)
            pb_request = document_processor_service.GetEvaluationRequest.pb(request)
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
            resp = evaluation.Evaluation()
            pb_resp = evaluation.Evaluation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_evaluation(resp)
            return resp

    class _GetProcessor(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("GetProcessor")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.GetProcessorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> processor.Processor:
            r"""Call the get processor method over HTTP.

            Args:
                request (~.document_processor_service.GetProcessorRequest):
                    The request object. Request message for get processor.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.processor.Processor:
                    The first-class citizen for Document
                AI. Each processor defines how to
                extract structural information from a
                document.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_processor(request, metadata)
            pb_request = document_processor_service.GetProcessorRequest.pb(request)
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
            resp = processor.Processor()
            pb_resp = processor.Processor.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_processor(resp)
            return resp

    class _GetProcessorType(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("GetProcessorType")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.GetProcessorTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> processor_type.ProcessorType:
            r"""Call the get processor type method over HTTP.

            Args:
                request (~.document_processor_service.GetProcessorTypeRequest):
                    The request object. Request message for get processor.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.processor_type.ProcessorType:
                    A processor type is responsible for
                performing a certain document
                understanding task on a certain type of
                document.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{name=projects/*/locations/*/processorTypes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_processor_type(
                request, metadata
            )
            pb_request = document_processor_service.GetProcessorTypeRequest.pb(request)
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
            resp = processor_type.ProcessorType()
            pb_resp = processor_type.ProcessorType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_processor_type(resp)
            return resp

    class _GetProcessorVersion(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("GetProcessorVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.GetProcessorVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> processor.ProcessorVersion:
            r"""Call the get processor version method over HTTP.

            Args:
                request (~.document_processor_service.GetProcessorVersionRequest):
                    The request object. Request message for get processor
                version.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.processor.ProcessorVersion:
                    A processor version is an
                implementation of a processor. Each
                processor can have multiple versions,
                pre-trained by Google internally or
                up-trained by the customer. At a time, a
                processor can only have one default
                version version. So the processor's
                behavior (when processing documents) is
                defined by a default version

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*/processorVersions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_processor_version(
                request, metadata
            )
            pb_request = document_processor_service.GetProcessorVersionRequest.pb(
                request
            )
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
            resp = processor.ProcessorVersion()
            pb_resp = processor.ProcessorVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_processor_version(resp)
            return resp

    class _ListEvaluations(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("ListEvaluations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.ListEvaluationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_processor_service.ListEvaluationsResponse:
            r"""Call the list evaluations method over HTTP.

            Args:
                request (~.document_processor_service.ListEvaluationsRequest):
                    The request object. Retrieves a list of evaluations for a
                given ProcessorVersion.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_processor_service.ListEvaluationsResponse:
                    The response from ListEvaluations.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{parent=projects/*/locations/*/processors/*/processorVersions/*}/evaluations",
                },
            ]
            request, metadata = self._interceptor.pre_list_evaluations(
                request, metadata
            )
            pb_request = document_processor_service.ListEvaluationsRequest.pb(request)
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
            resp = document_processor_service.ListEvaluationsResponse()
            pb_resp = document_processor_service.ListEvaluationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_evaluations(resp)
            return resp

    class _ListProcessors(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("ListProcessors")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.ListProcessorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_processor_service.ListProcessorsResponse:
            r"""Call the list processors method over HTTP.

            Args:
                request (~.document_processor_service.ListProcessorsRequest):
                    The request object. Request message for list all
                processors belongs to a project.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_processor_service.ListProcessorsResponse:
                    Response message for list processors.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{parent=projects/*/locations/*}/processors",
                },
            ]
            request, metadata = self._interceptor.pre_list_processors(request, metadata)
            pb_request = document_processor_service.ListProcessorsRequest.pb(request)
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
            resp = document_processor_service.ListProcessorsResponse()
            pb_resp = document_processor_service.ListProcessorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_processors(resp)
            return resp

    class _ListProcessorTypes(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("ListProcessorTypes")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.ListProcessorTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_processor_service.ListProcessorTypesResponse:
            r"""Call the list processor types method over HTTP.

            Args:
                request (~.document_processor_service.ListProcessorTypesRequest):
                    The request object. Request message for list processor
                types.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_processor_service.ListProcessorTypesResponse:
                    Response message for list processor
                types.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{parent=projects/*/locations/*}/processorTypes",
                },
            ]
            request, metadata = self._interceptor.pre_list_processor_types(
                request, metadata
            )
            pb_request = document_processor_service.ListProcessorTypesRequest.pb(
                request
            )
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
            resp = document_processor_service.ListProcessorTypesResponse()
            pb_resp = document_processor_service.ListProcessorTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_processor_types(resp)
            return resp

    class _ListProcessorVersions(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("ListProcessorVersions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.ListProcessorVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_processor_service.ListProcessorVersionsResponse:
            r"""Call the list processor versions method over HTTP.

            Args:
                request (~.document_processor_service.ListProcessorVersionsRequest):
                    The request object. Request message for list all
                processor versions belongs to a
                processor.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_processor_service.ListProcessorVersionsResponse:
                    Response message for list processors.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta3/{parent=projects/*/locations/*/processors/*}/processorVersions",
                },
            ]
            request, metadata = self._interceptor.pre_list_processor_versions(
                request, metadata
            )
            pb_request = document_processor_service.ListProcessorVersionsRequest.pb(
                request
            )
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
            resp = document_processor_service.ListProcessorVersionsResponse()
            pb_resp = document_processor_service.ListProcessorVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_processor_versions(resp)
            return resp

    class _ProcessDocument(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("ProcessDocument")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.ProcessRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_processor_service.ProcessResponse:
            r"""Call the process document method over HTTP.

            Args:
                request (~.document_processor_service.ProcessRequest):
                    The request object. Request message for the process
                document method.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_processor_service.ProcessResponse:
                    Response message for the process
                document method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*}:process",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*/processorVersions/*}:process",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_process_document(
                request, metadata
            )
            pb_request = document_processor_service.ProcessRequest.pb(request)
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
            resp = document_processor_service.ProcessResponse()
            pb_resp = document_processor_service.ProcessResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_process_document(resp)
            return resp

    class _ReviewDocument(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("ReviewDocument")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.ReviewDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the review document method over HTTP.

            Args:
                request (~.document_processor_service.ReviewDocumentRequest):
                    The request object. Request message for review document
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
                    "uri": "/v1beta3/{human_review_config=projects/*/locations/*/processors/*/humanReviewConfig}:reviewDocument",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_review_document(request, metadata)
            pb_request = document_processor_service.ReviewDocumentRequest.pb(request)
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
            resp = self._interceptor.post_review_document(resp)
            return resp

    class _SetDefaultProcessorVersion(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("SetDefaultProcessorVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.SetDefaultProcessorVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the set default processor
            version method over HTTP.

                Args:
                    request (~.document_processor_service.SetDefaultProcessorVersionRequest):
                        The request object. Request message for the set default
                    processor version method.

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
                    "uri": "/v1beta3/{processor=projects/*/locations/*/processors/*}:setDefaultProcessorVersion",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_default_processor_version(
                request, metadata
            )
            pb_request = (
                document_processor_service.SetDefaultProcessorVersionRequest.pb(request)
            )
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
            resp = self._interceptor.post_set_default_processor_version(resp)
            return resp

    class _TrainProcessorVersion(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("TrainProcessorVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.TrainProcessorVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the train processor version method over HTTP.

            Args:
                request (~.document_processor_service.TrainProcessorVersionRequest):
                    The request object. Request message for the create
                processor version method.

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
                    "uri": "/v1beta3/{parent=projects/*/locations/*/processors/*}/processorVersions:train",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_train_processor_version(
                request, metadata
            )
            pb_request = document_processor_service.TrainProcessorVersionRequest.pb(
                request
            )
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
            resp = self._interceptor.post_train_processor_version(resp)
            return resp

    class _UndeployProcessorVersion(DocumentProcessorServiceRestStub):
        def __hash__(self):
            return hash("UndeployProcessorVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: document_processor_service.UndeployProcessorVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undeploy processor
            version method over HTTP.

                Args:
                    request (~.document_processor_service.UndeployProcessorVersionRequest):
                        The request object. Request message for the undeploy
                    processor version method.

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
                    "uri": "/v1beta3/{name=projects/*/locations/*/processors/*/processorVersions/*}:undeploy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undeploy_processor_version(
                request, metadata
            )
            pb_request = document_processor_service.UndeployProcessorVersionRequest.pb(
                request
            )
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
            resp = self._interceptor.post_undeploy_processor_version(resp)
            return resp

    @property
    def batch_process_documents(
        self,
    ) -> Callable[
        [document_processor_service.BatchProcessRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchProcessDocuments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_processor(
        self,
    ) -> Callable[
        [document_processor_service.CreateProcessorRequest], gcd_processor.Processor
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_processor(
        self,
    ) -> Callable[
        [document_processor_service.DeleteProcessorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.DeleteProcessorVersionRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProcessorVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def deploy_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.DeployProcessorVersionRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeployProcessorVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_processor(
        self,
    ) -> Callable[
        [document_processor_service.DisableProcessorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_processor(
        self,
    ) -> Callable[
        [document_processor_service.EnableProcessorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def evaluate_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.EvaluateProcessorVersionRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EvaluateProcessorVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_processor_types(
        self,
    ) -> Callable[
        [document_processor_service.FetchProcessorTypesRequest],
        document_processor_service.FetchProcessorTypesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchProcessorTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_evaluation(
        self,
    ) -> Callable[
        [document_processor_service.GetEvaluationRequest], evaluation.Evaluation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEvaluation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_processor(
        self,
    ) -> Callable[
        [document_processor_service.GetProcessorRequest], processor.Processor
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProcessor(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_processor_type(
        self,
    ) -> Callable[
        [document_processor_service.GetProcessorTypeRequest],
        processor_type.ProcessorType,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProcessorType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.GetProcessorVersionRequest],
        processor.ProcessorVersion,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProcessorVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_evaluations(
        self,
    ) -> Callable[
        [document_processor_service.ListEvaluationsRequest],
        document_processor_service.ListEvaluationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEvaluations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_processors(
        self,
    ) -> Callable[
        [document_processor_service.ListProcessorsRequest],
        document_processor_service.ListProcessorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProcessors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_processor_types(
        self,
    ) -> Callable[
        [document_processor_service.ListProcessorTypesRequest],
        document_processor_service.ListProcessorTypesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProcessorTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_processor_versions(
        self,
    ) -> Callable[
        [document_processor_service.ListProcessorVersionsRequest],
        document_processor_service.ListProcessorVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProcessorVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def process_document(
        self,
    ) -> Callable[
        [document_processor_service.ProcessRequest],
        document_processor_service.ProcessResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ProcessDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def review_document(
        self,
    ) -> Callable[
        [document_processor_service.ReviewDocumentRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReviewDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_default_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.SetDefaultProcessorVersionRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetDefaultProcessorVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def train_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.TrainProcessorVersionRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TrainProcessorVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undeploy_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.UndeployProcessorVersionRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeployProcessorVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(DocumentProcessorServiceRestStub):
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
                    "uri": "/v1beta3/{name=projects/*/locations/*}",
                },
                {
                    "method": "get",
                    "uri": "/uiv1beta3/{name=projects/*/locations/*}",
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

    class _ListLocations(DocumentProcessorServiceRestStub):
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
                    "uri": "/v1beta3/{name=projects/*}/locations",
                },
                {
                    "method": "get",
                    "uri": "/uiv1beta3/{name=projects/*}/locations",
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

    class _CancelOperation(DocumentProcessorServiceRestStub):
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
                    "uri": "/v1beta3/{name=projects/*/locations/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/uiv1beta3/{name=projects/*/locations/*/operations/*}:cancel",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(DocumentProcessorServiceRestStub):
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
                    "uri": "/v1beta3/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/uiv1beta3/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(DocumentProcessorServiceRestStub):
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
                    "uri": "/v1beta3/{name=projects/*/locations/*/operations}",
                },
                {
                    "method": "get",
                    "uri": "/uiv1beta3/{name=projects/*/locations/*/operations}",
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


__all__ = ("DocumentProcessorServiceRestTransport",)
