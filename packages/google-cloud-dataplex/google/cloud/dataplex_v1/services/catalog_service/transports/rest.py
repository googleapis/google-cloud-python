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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dataplex_v1.types import catalog

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCatalogServiceRestTransport

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


class CatalogServiceRestInterceptor:
    """Interceptor for CatalogService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CatalogServiceRestTransport.

    .. code-block:: python
        class MyCustomCatalogServiceInterceptor(CatalogServiceRestInterceptor):
            def pre_cancel_metadata_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_create_aspect_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_aspect_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_entry_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_entry_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_entry_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_entry_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_metadata_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_metadata_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_aspect_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_aspect_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_entry_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_entry_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_entry_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_entry_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_aspect_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_aspect_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_entry_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_entry_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_entry_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_entry_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_metadata_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_metadata_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_aspect_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_aspect_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_entries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_entries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_entry_groups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_entry_groups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_entry_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_entry_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_metadata_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_metadata_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lookup_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lookup_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_entries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_entries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_aspect_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_aspect_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_entry_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_entry_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_entry_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_entry_type(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CatalogServiceRestTransport(interceptor=MyCustomCatalogServiceInterceptor())
        client = CatalogServiceClient(transport=transport)


    """

    def pre_cancel_metadata_job(
        self,
        request: catalog.CancelMetadataJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.CancelMetadataJobRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_metadata_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def pre_create_aspect_type(
        self,
        request: catalog.CreateAspectTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.CreateAspectTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_aspect_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_create_aspect_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_aspect_type

        DEPRECATED. Please use the `post_create_aspect_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_create_aspect_type` interceptor runs
        before the `post_create_aspect_type_with_metadata` interceptor.
        """
        return response

    def post_create_aspect_type_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_aspect_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_create_aspect_type_with_metadata`
        interceptor in new development instead of the `post_create_aspect_type` interceptor.
        When both interceptors are used, this `post_create_aspect_type_with_metadata` interceptor runs after the
        `post_create_aspect_type` interceptor. The (possibly modified) response returned by
        `post_create_aspect_type` will be passed to
        `post_create_aspect_type_with_metadata`.
        """
        return response, metadata

    def pre_create_entry(
        self,
        request: catalog.CreateEntryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.CreateEntryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_create_entry(self, response: catalog.Entry) -> catalog.Entry:
        """Post-rpc interceptor for create_entry

        DEPRECATED. Please use the `post_create_entry_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_create_entry` interceptor runs
        before the `post_create_entry_with_metadata` interceptor.
        """
        return response

    def post_create_entry_with_metadata(
        self, response: catalog.Entry, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[catalog.Entry, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_entry

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_create_entry_with_metadata`
        interceptor in new development instead of the `post_create_entry` interceptor.
        When both interceptors are used, this `post_create_entry_with_metadata` interceptor runs after the
        `post_create_entry` interceptor. The (possibly modified) response returned by
        `post_create_entry` will be passed to
        `post_create_entry_with_metadata`.
        """
        return response, metadata

    def pre_create_entry_group(
        self,
        request: catalog.CreateEntryGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.CreateEntryGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_entry_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_create_entry_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_entry_group

        DEPRECATED. Please use the `post_create_entry_group_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_create_entry_group` interceptor runs
        before the `post_create_entry_group_with_metadata` interceptor.
        """
        return response

    def post_create_entry_group_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_entry_group

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_create_entry_group_with_metadata`
        interceptor in new development instead of the `post_create_entry_group` interceptor.
        When both interceptors are used, this `post_create_entry_group_with_metadata` interceptor runs after the
        `post_create_entry_group` interceptor. The (possibly modified) response returned by
        `post_create_entry_group` will be passed to
        `post_create_entry_group_with_metadata`.
        """
        return response, metadata

    def pre_create_entry_type(
        self,
        request: catalog.CreateEntryTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.CreateEntryTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_entry_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_create_entry_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_entry_type

        DEPRECATED. Please use the `post_create_entry_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_create_entry_type` interceptor runs
        before the `post_create_entry_type_with_metadata` interceptor.
        """
        return response

    def post_create_entry_type_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_entry_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_create_entry_type_with_metadata`
        interceptor in new development instead of the `post_create_entry_type` interceptor.
        When both interceptors are used, this `post_create_entry_type_with_metadata` interceptor runs after the
        `post_create_entry_type` interceptor. The (possibly modified) response returned by
        `post_create_entry_type` will be passed to
        `post_create_entry_type_with_metadata`.
        """
        return response, metadata

    def pre_create_metadata_job(
        self,
        request: catalog.CreateMetadataJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.CreateMetadataJobRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_metadata_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_create_metadata_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_metadata_job

        DEPRECATED. Please use the `post_create_metadata_job_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_create_metadata_job` interceptor runs
        before the `post_create_metadata_job_with_metadata` interceptor.
        """
        return response

    def post_create_metadata_job_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_metadata_job

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_create_metadata_job_with_metadata`
        interceptor in new development instead of the `post_create_metadata_job` interceptor.
        When both interceptors are used, this `post_create_metadata_job_with_metadata` interceptor runs after the
        `post_create_metadata_job` interceptor. The (possibly modified) response returned by
        `post_create_metadata_job` will be passed to
        `post_create_metadata_job_with_metadata`.
        """
        return response, metadata

    def pre_delete_aspect_type(
        self,
        request: catalog.DeleteAspectTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.DeleteAspectTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_aspect_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_delete_aspect_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_aspect_type

        DEPRECATED. Please use the `post_delete_aspect_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_delete_aspect_type` interceptor runs
        before the `post_delete_aspect_type_with_metadata` interceptor.
        """
        return response

    def post_delete_aspect_type_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_aspect_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_delete_aspect_type_with_metadata`
        interceptor in new development instead of the `post_delete_aspect_type` interceptor.
        When both interceptors are used, this `post_delete_aspect_type_with_metadata` interceptor runs after the
        `post_delete_aspect_type` interceptor. The (possibly modified) response returned by
        `post_delete_aspect_type` will be passed to
        `post_delete_aspect_type_with_metadata`.
        """
        return response, metadata

    def pre_delete_entry(
        self,
        request: catalog.DeleteEntryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.DeleteEntryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_delete_entry(self, response: catalog.Entry) -> catalog.Entry:
        """Post-rpc interceptor for delete_entry

        DEPRECATED. Please use the `post_delete_entry_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_delete_entry` interceptor runs
        before the `post_delete_entry_with_metadata` interceptor.
        """
        return response

    def post_delete_entry_with_metadata(
        self, response: catalog.Entry, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[catalog.Entry, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_entry

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_delete_entry_with_metadata`
        interceptor in new development instead of the `post_delete_entry` interceptor.
        When both interceptors are used, this `post_delete_entry_with_metadata` interceptor runs after the
        `post_delete_entry` interceptor. The (possibly modified) response returned by
        `post_delete_entry` will be passed to
        `post_delete_entry_with_metadata`.
        """
        return response, metadata

    def pre_delete_entry_group(
        self,
        request: catalog.DeleteEntryGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.DeleteEntryGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_entry_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_delete_entry_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_entry_group

        DEPRECATED. Please use the `post_delete_entry_group_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_delete_entry_group` interceptor runs
        before the `post_delete_entry_group_with_metadata` interceptor.
        """
        return response

    def post_delete_entry_group_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_entry_group

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_delete_entry_group_with_metadata`
        interceptor in new development instead of the `post_delete_entry_group` interceptor.
        When both interceptors are used, this `post_delete_entry_group_with_metadata` interceptor runs after the
        `post_delete_entry_group` interceptor. The (possibly modified) response returned by
        `post_delete_entry_group` will be passed to
        `post_delete_entry_group_with_metadata`.
        """
        return response, metadata

    def pre_delete_entry_type(
        self,
        request: catalog.DeleteEntryTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.DeleteEntryTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_entry_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_delete_entry_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_entry_type

        DEPRECATED. Please use the `post_delete_entry_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_delete_entry_type` interceptor runs
        before the `post_delete_entry_type_with_metadata` interceptor.
        """
        return response

    def post_delete_entry_type_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_entry_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_delete_entry_type_with_metadata`
        interceptor in new development instead of the `post_delete_entry_type` interceptor.
        When both interceptors are used, this `post_delete_entry_type_with_metadata` interceptor runs after the
        `post_delete_entry_type` interceptor. The (possibly modified) response returned by
        `post_delete_entry_type` will be passed to
        `post_delete_entry_type_with_metadata`.
        """
        return response, metadata

    def pre_get_aspect_type(
        self,
        request: catalog.GetAspectTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.GetAspectTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_aspect_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_aspect_type(self, response: catalog.AspectType) -> catalog.AspectType:
        """Post-rpc interceptor for get_aspect_type

        DEPRECATED. Please use the `post_get_aspect_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_get_aspect_type` interceptor runs
        before the `post_get_aspect_type_with_metadata` interceptor.
        """
        return response

    def post_get_aspect_type_with_metadata(
        self,
        response: catalog.AspectType,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.AspectType, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_aspect_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_get_aspect_type_with_metadata`
        interceptor in new development instead of the `post_get_aspect_type` interceptor.
        When both interceptors are used, this `post_get_aspect_type_with_metadata` interceptor runs after the
        `post_get_aspect_type` interceptor. The (possibly modified) response returned by
        `post_get_aspect_type` will be passed to
        `post_get_aspect_type_with_metadata`.
        """
        return response, metadata

    def pre_get_entry(
        self,
        request: catalog.GetEntryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.GetEntryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_entry(self, response: catalog.Entry) -> catalog.Entry:
        """Post-rpc interceptor for get_entry

        DEPRECATED. Please use the `post_get_entry_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_get_entry` interceptor runs
        before the `post_get_entry_with_metadata` interceptor.
        """
        return response

    def post_get_entry_with_metadata(
        self, response: catalog.Entry, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[catalog.Entry, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_entry

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_get_entry_with_metadata`
        interceptor in new development instead of the `post_get_entry` interceptor.
        When both interceptors are used, this `post_get_entry_with_metadata` interceptor runs after the
        `post_get_entry` interceptor. The (possibly modified) response returned by
        `post_get_entry` will be passed to
        `post_get_entry_with_metadata`.
        """
        return response, metadata

    def pre_get_entry_group(
        self,
        request: catalog.GetEntryGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.GetEntryGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_entry_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_entry_group(self, response: catalog.EntryGroup) -> catalog.EntryGroup:
        """Post-rpc interceptor for get_entry_group

        DEPRECATED. Please use the `post_get_entry_group_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_get_entry_group` interceptor runs
        before the `post_get_entry_group_with_metadata` interceptor.
        """
        return response

    def post_get_entry_group_with_metadata(
        self,
        response: catalog.EntryGroup,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.EntryGroup, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_entry_group

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_get_entry_group_with_metadata`
        interceptor in new development instead of the `post_get_entry_group` interceptor.
        When both interceptors are used, this `post_get_entry_group_with_metadata` interceptor runs after the
        `post_get_entry_group` interceptor. The (possibly modified) response returned by
        `post_get_entry_group` will be passed to
        `post_get_entry_group_with_metadata`.
        """
        return response, metadata

    def pre_get_entry_type(
        self,
        request: catalog.GetEntryTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.GetEntryTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_entry_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_entry_type(self, response: catalog.EntryType) -> catalog.EntryType:
        """Post-rpc interceptor for get_entry_type

        DEPRECATED. Please use the `post_get_entry_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_get_entry_type` interceptor runs
        before the `post_get_entry_type_with_metadata` interceptor.
        """
        return response

    def post_get_entry_type_with_metadata(
        self,
        response: catalog.EntryType,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.EntryType, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_entry_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_get_entry_type_with_metadata`
        interceptor in new development instead of the `post_get_entry_type` interceptor.
        When both interceptors are used, this `post_get_entry_type_with_metadata` interceptor runs after the
        `post_get_entry_type` interceptor. The (possibly modified) response returned by
        `post_get_entry_type` will be passed to
        `post_get_entry_type_with_metadata`.
        """
        return response, metadata

    def pre_get_metadata_job(
        self,
        request: catalog.GetMetadataJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.GetMetadataJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_metadata_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_metadata_job(
        self, response: catalog.MetadataJob
    ) -> catalog.MetadataJob:
        """Post-rpc interceptor for get_metadata_job

        DEPRECATED. Please use the `post_get_metadata_job_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_get_metadata_job` interceptor runs
        before the `post_get_metadata_job_with_metadata` interceptor.
        """
        return response

    def post_get_metadata_job_with_metadata(
        self,
        response: catalog.MetadataJob,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.MetadataJob, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_metadata_job

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_get_metadata_job_with_metadata`
        interceptor in new development instead of the `post_get_metadata_job` interceptor.
        When both interceptors are used, this `post_get_metadata_job_with_metadata` interceptor runs after the
        `post_get_metadata_job` interceptor. The (possibly modified) response returned by
        `post_get_metadata_job` will be passed to
        `post_get_metadata_job_with_metadata`.
        """
        return response, metadata

    def pre_list_aspect_types(
        self,
        request: catalog.ListAspectTypesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.ListAspectTypesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_aspect_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_aspect_types(
        self, response: catalog.ListAspectTypesResponse
    ) -> catalog.ListAspectTypesResponse:
        """Post-rpc interceptor for list_aspect_types

        DEPRECATED. Please use the `post_list_aspect_types_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_list_aspect_types` interceptor runs
        before the `post_list_aspect_types_with_metadata` interceptor.
        """
        return response

    def post_list_aspect_types_with_metadata(
        self,
        response: catalog.ListAspectTypesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.ListAspectTypesResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_aspect_types

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_list_aspect_types_with_metadata`
        interceptor in new development instead of the `post_list_aspect_types` interceptor.
        When both interceptors are used, this `post_list_aspect_types_with_metadata` interceptor runs after the
        `post_list_aspect_types` interceptor. The (possibly modified) response returned by
        `post_list_aspect_types` will be passed to
        `post_list_aspect_types_with_metadata`.
        """
        return response, metadata

    def pre_list_entries(
        self,
        request: catalog.ListEntriesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.ListEntriesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_entries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_entries(
        self, response: catalog.ListEntriesResponse
    ) -> catalog.ListEntriesResponse:
        """Post-rpc interceptor for list_entries

        DEPRECATED. Please use the `post_list_entries_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_list_entries` interceptor runs
        before the `post_list_entries_with_metadata` interceptor.
        """
        return response

    def post_list_entries_with_metadata(
        self,
        response: catalog.ListEntriesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.ListEntriesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_entries

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_list_entries_with_metadata`
        interceptor in new development instead of the `post_list_entries` interceptor.
        When both interceptors are used, this `post_list_entries_with_metadata` interceptor runs after the
        `post_list_entries` interceptor. The (possibly modified) response returned by
        `post_list_entries` will be passed to
        `post_list_entries_with_metadata`.
        """
        return response, metadata

    def pre_list_entry_groups(
        self,
        request: catalog.ListEntryGroupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.ListEntryGroupsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_entry_groups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_entry_groups(
        self, response: catalog.ListEntryGroupsResponse
    ) -> catalog.ListEntryGroupsResponse:
        """Post-rpc interceptor for list_entry_groups

        DEPRECATED. Please use the `post_list_entry_groups_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_list_entry_groups` interceptor runs
        before the `post_list_entry_groups_with_metadata` interceptor.
        """
        return response

    def post_list_entry_groups_with_metadata(
        self,
        response: catalog.ListEntryGroupsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.ListEntryGroupsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_entry_groups

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_list_entry_groups_with_metadata`
        interceptor in new development instead of the `post_list_entry_groups` interceptor.
        When both interceptors are used, this `post_list_entry_groups_with_metadata` interceptor runs after the
        `post_list_entry_groups` interceptor. The (possibly modified) response returned by
        `post_list_entry_groups` will be passed to
        `post_list_entry_groups_with_metadata`.
        """
        return response, metadata

    def pre_list_entry_types(
        self,
        request: catalog.ListEntryTypesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.ListEntryTypesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_entry_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_entry_types(
        self, response: catalog.ListEntryTypesResponse
    ) -> catalog.ListEntryTypesResponse:
        """Post-rpc interceptor for list_entry_types

        DEPRECATED. Please use the `post_list_entry_types_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_list_entry_types` interceptor runs
        before the `post_list_entry_types_with_metadata` interceptor.
        """
        return response

    def post_list_entry_types_with_metadata(
        self,
        response: catalog.ListEntryTypesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.ListEntryTypesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_entry_types

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_list_entry_types_with_metadata`
        interceptor in new development instead of the `post_list_entry_types` interceptor.
        When both interceptors are used, this `post_list_entry_types_with_metadata` interceptor runs after the
        `post_list_entry_types` interceptor. The (possibly modified) response returned by
        `post_list_entry_types` will be passed to
        `post_list_entry_types_with_metadata`.
        """
        return response, metadata

    def pre_list_metadata_jobs(
        self,
        request: catalog.ListMetadataJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.ListMetadataJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_metadata_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_metadata_jobs(
        self, response: catalog.ListMetadataJobsResponse
    ) -> catalog.ListMetadataJobsResponse:
        """Post-rpc interceptor for list_metadata_jobs

        DEPRECATED. Please use the `post_list_metadata_jobs_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_list_metadata_jobs` interceptor runs
        before the `post_list_metadata_jobs_with_metadata` interceptor.
        """
        return response

    def post_list_metadata_jobs_with_metadata(
        self,
        response: catalog.ListMetadataJobsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.ListMetadataJobsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_metadata_jobs

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_list_metadata_jobs_with_metadata`
        interceptor in new development instead of the `post_list_metadata_jobs` interceptor.
        When both interceptors are used, this `post_list_metadata_jobs_with_metadata` interceptor runs after the
        `post_list_metadata_jobs` interceptor. The (possibly modified) response returned by
        `post_list_metadata_jobs` will be passed to
        `post_list_metadata_jobs_with_metadata`.
        """
        return response, metadata

    def pre_lookup_entry(
        self,
        request: catalog.LookupEntryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.LookupEntryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for lookup_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_lookup_entry(self, response: catalog.Entry) -> catalog.Entry:
        """Post-rpc interceptor for lookup_entry

        DEPRECATED. Please use the `post_lookup_entry_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_lookup_entry` interceptor runs
        before the `post_lookup_entry_with_metadata` interceptor.
        """
        return response

    def post_lookup_entry_with_metadata(
        self, response: catalog.Entry, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[catalog.Entry, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for lookup_entry

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_lookup_entry_with_metadata`
        interceptor in new development instead of the `post_lookup_entry` interceptor.
        When both interceptors are used, this `post_lookup_entry_with_metadata` interceptor runs after the
        `post_lookup_entry` interceptor. The (possibly modified) response returned by
        `post_lookup_entry` will be passed to
        `post_lookup_entry_with_metadata`.
        """
        return response, metadata

    def pre_search_entries(
        self,
        request: catalog.SearchEntriesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.SearchEntriesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for search_entries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_search_entries(
        self, response: catalog.SearchEntriesResponse
    ) -> catalog.SearchEntriesResponse:
        """Post-rpc interceptor for search_entries

        DEPRECATED. Please use the `post_search_entries_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_search_entries` interceptor runs
        before the `post_search_entries_with_metadata` interceptor.
        """
        return response

    def post_search_entries_with_metadata(
        self,
        response: catalog.SearchEntriesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.SearchEntriesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for search_entries

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_search_entries_with_metadata`
        interceptor in new development instead of the `post_search_entries` interceptor.
        When both interceptors are used, this `post_search_entries_with_metadata` interceptor runs after the
        `post_search_entries` interceptor. The (possibly modified) response returned by
        `post_search_entries` will be passed to
        `post_search_entries_with_metadata`.
        """
        return response, metadata

    def pre_update_aspect_type(
        self,
        request: catalog.UpdateAspectTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.UpdateAspectTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_aspect_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_aspect_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_aspect_type

        DEPRECATED. Please use the `post_update_aspect_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_update_aspect_type` interceptor runs
        before the `post_update_aspect_type_with_metadata` interceptor.
        """
        return response

    def post_update_aspect_type_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_aspect_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_update_aspect_type_with_metadata`
        interceptor in new development instead of the `post_update_aspect_type` interceptor.
        When both interceptors are used, this `post_update_aspect_type_with_metadata` interceptor runs after the
        `post_update_aspect_type` interceptor. The (possibly modified) response returned by
        `post_update_aspect_type` will be passed to
        `post_update_aspect_type_with_metadata`.
        """
        return response, metadata

    def pre_update_entry(
        self,
        request: catalog.UpdateEntryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.UpdateEntryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_entry(self, response: catalog.Entry) -> catalog.Entry:
        """Post-rpc interceptor for update_entry

        DEPRECATED. Please use the `post_update_entry_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_update_entry` interceptor runs
        before the `post_update_entry_with_metadata` interceptor.
        """
        return response

    def post_update_entry_with_metadata(
        self, response: catalog.Entry, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[catalog.Entry, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_entry

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_update_entry_with_metadata`
        interceptor in new development instead of the `post_update_entry` interceptor.
        When both interceptors are used, this `post_update_entry_with_metadata` interceptor runs after the
        `post_update_entry` interceptor. The (possibly modified) response returned by
        `post_update_entry` will be passed to
        `post_update_entry_with_metadata`.
        """
        return response, metadata

    def pre_update_entry_group(
        self,
        request: catalog.UpdateEntryGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        catalog.UpdateEntryGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_entry_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_entry_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_entry_group

        DEPRECATED. Please use the `post_update_entry_group_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_update_entry_group` interceptor runs
        before the `post_update_entry_group_with_metadata` interceptor.
        """
        return response

    def post_update_entry_group_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_entry_group

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_update_entry_group_with_metadata`
        interceptor in new development instead of the `post_update_entry_group` interceptor.
        When both interceptors are used, this `post_update_entry_group_with_metadata` interceptor runs after the
        `post_update_entry_group` interceptor. The (possibly modified) response returned by
        `post_update_entry_group` will be passed to
        `post_update_entry_group_with_metadata`.
        """
        return response, metadata

    def pre_update_entry_type(
        self,
        request: catalog.UpdateEntryTypeRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[catalog.UpdateEntryTypeRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_entry_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_update_entry_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_entry_type

        DEPRECATED. Please use the `post_update_entry_type_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code. This `post_update_entry_type` interceptor runs
        before the `post_update_entry_type_with_metadata` interceptor.
        """
        return response

    def post_update_entry_type_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_entry_type

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CatalogService server but before it is returned to user code.

        We recommend only using this `post_update_entry_type_with_metadata`
        interceptor in new development instead of the `post_update_entry_type` interceptor.
        When both interceptors are used, this `post_update_entry_type_with_metadata` interceptor runs after the
        `post_update_entry_type` interceptor. The (possibly modified) response returned by
        `post_update_entry_type` will be passed to
        `post_update_entry_type_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CatalogService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the CatalogService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CatalogServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CatalogServiceRestInterceptor


class CatalogServiceRestTransport(_BaseCatalogServiceRestTransport):
    """REST backend synchronous transport for CatalogService.

    The primary resources offered by this service are
    EntryGroups, EntryTypes, AspectTypes, and Entries. They
    collectively let data administrators organize, manage, secure,
    and catalog data located across cloud projects in their
    organization in a variety of storage systems, including Cloud
    Storage and BigQuery.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dataplex.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CatalogServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dataplex.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CatalogServiceRestInterceptor()
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
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                    {
                        "method": "post",
                        "uri": "/v1/{name=organizations/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "delete",
                        "uri": "/v1/{name=organizations/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=organizations/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=organizations/*/locations/*/operations/*}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CancelMetadataJob(
        _BaseCatalogServiceRestTransport._BaseCancelMetadataJob, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CancelMetadataJob")

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
            request: catalog.CancelMetadataJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the cancel metadata job method over HTTP.

            Args:
                request (~.catalog.CancelMetadataJobRequest):
                    The request object. Cancel metadata job request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCancelMetadataJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_metadata_job(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCancelMetadataJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCancelMetadataJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCancelMetadataJob._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.CancelMetadataJob",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CancelMetadataJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CancelMetadataJob._get_response(
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

    class _CreateAspectType(
        _BaseCatalogServiceRestTransport._BaseCreateAspectType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CreateAspectType")

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
            request: catalog.CreateAspectTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create aspect type method over HTTP.

            Args:
                request (~.catalog.CreateAspectTypeRequest):
                    The request object. Create AspectType Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCreateAspectType._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_aspect_type(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCreateAspectType._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCreateAspectType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCreateAspectType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.CreateAspectType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateAspectType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CreateAspectType._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_aspect_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_aspect_type_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.create_aspect_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateAspectType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateEntry(
        _BaseCatalogServiceRestTransport._BaseCreateEntry, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CreateEntry")

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
            request: catalog.CreateEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.Entry:
            r"""Call the create entry method over HTTP.

            Args:
                request (~.catalog.CreateEntryRequest):
                    The request object. Create Entry request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.Entry:
                    An entry is a representation of a
                data resource that can be described by
                various metadata.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCreateEntry._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_entry(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCreateEntry._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCreateEntry._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCreateEntry._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.CreateEntry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateEntry",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CreateEntry._get_response(
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
            resp = catalog.Entry()
            pb_resp = catalog.Entry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_entry(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_entry_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.Entry.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.create_entry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateEntry",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateEntryGroup(
        _BaseCatalogServiceRestTransport._BaseCreateEntryGroup, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CreateEntryGroup")

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
            request: catalog.CreateEntryGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create entry group method over HTTP.

            Args:
                request (~.catalog.CreateEntryGroupRequest):
                    The request object. Create EntryGroup Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCreateEntryGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_entry_group(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCreateEntryGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCreateEntryGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCreateEntryGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.CreateEntryGroup",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateEntryGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CreateEntryGroup._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_entry_group(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_entry_group_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.create_entry_group",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateEntryGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateEntryType(
        _BaseCatalogServiceRestTransport._BaseCreateEntryType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CreateEntryType")

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
            request: catalog.CreateEntryTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create entry type method over HTTP.

            Args:
                request (~.catalog.CreateEntryTypeRequest):
                    The request object. Create EntryType Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCreateEntryType._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_entry_type(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCreateEntryType._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCreateEntryType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCreateEntryType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.CreateEntryType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateEntryType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CreateEntryType._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_entry_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_entry_type_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.create_entry_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateEntryType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateMetadataJob(
        _BaseCatalogServiceRestTransport._BaseCreateMetadataJob, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CreateMetadataJob")

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
            request: catalog.CreateMetadataJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create metadata job method over HTTP.

            Args:
                request (~.catalog.CreateMetadataJobRequest):
                    The request object. Create metadata job request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCreateMetadataJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_metadata_job(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCreateMetadataJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCreateMetadataJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCreateMetadataJob._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.CreateMetadataJob",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateMetadataJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CreateMetadataJob._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_metadata_job(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_metadata_job_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.create_metadata_job",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CreateMetadataJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteAspectType(
        _BaseCatalogServiceRestTransport._BaseDeleteAspectType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.DeleteAspectType")

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
            request: catalog.DeleteAspectTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete aspect type method over HTTP.

            Args:
                request (~.catalog.DeleteAspectTypeRequest):
                    The request object. Delele AspectType Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseDeleteAspectType._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_aspect_type(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseDeleteAspectType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseDeleteAspectType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.DeleteAspectType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteAspectType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._DeleteAspectType._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_aspect_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_aspect_type_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.delete_aspect_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteAspectType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteEntry(
        _BaseCatalogServiceRestTransport._BaseDeleteEntry, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.DeleteEntry")

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
            request: catalog.DeleteEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.Entry:
            r"""Call the delete entry method over HTTP.

            Args:
                request (~.catalog.DeleteEntryRequest):
                    The request object. Delete Entry request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.Entry:
                    An entry is a representation of a
                data resource that can be described by
                various metadata.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseDeleteEntry._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_entry(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseDeleteEntry._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseDeleteEntry._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.DeleteEntry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteEntry",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._DeleteEntry._get_response(
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
            resp = catalog.Entry()
            pb_resp = catalog.Entry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_entry(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_entry_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.Entry.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.delete_entry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteEntry",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteEntryGroup(
        _BaseCatalogServiceRestTransport._BaseDeleteEntryGroup, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.DeleteEntryGroup")

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
            request: catalog.DeleteEntryGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete entry group method over HTTP.

            Args:
                request (~.catalog.DeleteEntryGroupRequest):
                    The request object. Delete EntryGroup Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseDeleteEntryGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_entry_group(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseDeleteEntryGroup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseDeleteEntryGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.DeleteEntryGroup",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteEntryGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._DeleteEntryGroup._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_entry_group(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_entry_group_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.delete_entry_group",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteEntryGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteEntryType(
        _BaseCatalogServiceRestTransport._BaseDeleteEntryType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.DeleteEntryType")

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
            request: catalog.DeleteEntryTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete entry type method over HTTP.

            Args:
                request (~.catalog.DeleteEntryTypeRequest):
                    The request object. Delele EntryType Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseDeleteEntryType._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_entry_type(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseDeleteEntryType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseDeleteEntryType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.DeleteEntryType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteEntryType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._DeleteEntryType._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_entry_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_entry_type_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.delete_entry_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteEntryType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetAspectType(
        _BaseCatalogServiceRestTransport._BaseGetAspectType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetAspectType")

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
            request: catalog.GetAspectTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.AspectType:
            r"""Call the get aspect type method over HTTP.

            Args:
                request (~.catalog.GetAspectTypeRequest):
                    The request object. Get AspectType request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.AspectType:
                    AspectType is a template for creating
                Aspects, and represents the JSON-schema
                for a given Entry, for example, BigQuery
                Table Schema.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseGetAspectType._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_aspect_type(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseGetAspectType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseGetAspectType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.GetAspectType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetAspectType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetAspectType._get_response(
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
            resp = catalog.AspectType()
            pb_resp = catalog.AspectType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_aspect_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_aspect_type_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.AspectType.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.get_aspect_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetAspectType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetEntry(
        _BaseCatalogServiceRestTransport._BaseGetEntry, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetEntry")

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
            request: catalog.GetEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.Entry:
            r"""Call the get entry method over HTTP.

            Args:
                request (~.catalog.GetEntryRequest):
                    The request object. Get Entry request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.Entry:
                    An entry is a representation of a
                data resource that can be described by
                various metadata.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseGetEntry._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_entry(request, metadata)
            transcoded_request = (
                _BaseCatalogServiceRestTransport._BaseGetEntry._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCatalogServiceRestTransport._BaseGetEntry._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.GetEntry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetEntry",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetEntry._get_response(
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
            resp = catalog.Entry()
            pb_resp = catalog.Entry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_entry(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_entry_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.Entry.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.get_entry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetEntry",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetEntryGroup(
        _BaseCatalogServiceRestTransport._BaseGetEntryGroup, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetEntryGroup")

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
            request: catalog.GetEntryGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.EntryGroup:
            r"""Call the get entry group method over HTTP.

            Args:
                request (~.catalog.GetEntryGroupRequest):
                    The request object. Get EntryGroup request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.EntryGroup:
                    An Entry Group represents a logical
                grouping of one or more Entries.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseGetEntryGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_entry_group(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseGetEntryGroup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseGetEntryGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.GetEntryGroup",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetEntryGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetEntryGroup._get_response(
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
            resp = catalog.EntryGroup()
            pb_resp = catalog.EntryGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_entry_group(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_entry_group_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.EntryGroup.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.get_entry_group",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetEntryGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetEntryType(
        _BaseCatalogServiceRestTransport._BaseGetEntryType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetEntryType")

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
            request: catalog.GetEntryTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.EntryType:
            r"""Call the get entry type method over HTTP.

            Args:
                request (~.catalog.GetEntryTypeRequest):
                    The request object. Get EntryType request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.EntryType:
                    Entry Type is a template for creating
                Entries.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseGetEntryType._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_entry_type(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseGetEntryType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseGetEntryType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.GetEntryType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetEntryType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetEntryType._get_response(
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
            resp = catalog.EntryType()
            pb_resp = catalog.EntryType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_entry_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_entry_type_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.EntryType.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.get_entry_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetEntryType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetMetadataJob(
        _BaseCatalogServiceRestTransport._BaseGetMetadataJob, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetMetadataJob")

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
            request: catalog.GetMetadataJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.MetadataJob:
            r"""Call the get metadata job method over HTTP.

            Args:
                request (~.catalog.GetMetadataJobRequest):
                    The request object. Get metadata job request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.MetadataJob:
                    A metadata job resource.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseGetMetadataJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_metadata_job(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseGetMetadataJob._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseGetMetadataJob._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.GetMetadataJob",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetMetadataJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetMetadataJob._get_response(
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
            resp = catalog.MetadataJob()
            pb_resp = catalog.MetadataJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_metadata_job(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_metadata_job_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.MetadataJob.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.get_metadata_job",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetMetadataJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAspectTypes(
        _BaseCatalogServiceRestTransport._BaseListAspectTypes, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListAspectTypes")

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
            request: catalog.ListAspectTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.ListAspectTypesResponse:
            r"""Call the list aspect types method over HTTP.

            Args:
                request (~.catalog.ListAspectTypesRequest):
                    The request object. List AspectTypes request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.ListAspectTypesResponse:
                    List AspectTypes response.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListAspectTypes._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_aspect_types(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListAspectTypes._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListAspectTypes._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.ListAspectTypes",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListAspectTypes",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListAspectTypes._get_response(
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
            resp = catalog.ListAspectTypesResponse()
            pb_resp = catalog.ListAspectTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_aspect_types(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_aspect_types_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.ListAspectTypesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.list_aspect_types",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListAspectTypes",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListEntries(
        _BaseCatalogServiceRestTransport._BaseListEntries, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListEntries")

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
            request: catalog.ListEntriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.ListEntriesResponse:
            r"""Call the list entries method over HTTP.

            Args:
                request (~.catalog.ListEntriesRequest):
                    The request object. List Entries request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.ListEntriesResponse:
                    List Entries response.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListEntries._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_entries(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListEntries._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListEntries._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.ListEntries",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListEntries",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListEntries._get_response(
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
            resp = catalog.ListEntriesResponse()
            pb_resp = catalog.ListEntriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_entries(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_entries_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.ListEntriesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.list_entries",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListEntries",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListEntryGroups(
        _BaseCatalogServiceRestTransport._BaseListEntryGroups, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListEntryGroups")

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
            request: catalog.ListEntryGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.ListEntryGroupsResponse:
            r"""Call the list entry groups method over HTTP.

            Args:
                request (~.catalog.ListEntryGroupsRequest):
                    The request object. List entryGroups request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.ListEntryGroupsResponse:
                    List entry groups response.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListEntryGroups._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_entry_groups(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListEntryGroups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListEntryGroups._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.ListEntryGroups",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListEntryGroups",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListEntryGroups._get_response(
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
            resp = catalog.ListEntryGroupsResponse()
            pb_resp = catalog.ListEntryGroupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_entry_groups(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_entry_groups_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.ListEntryGroupsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.list_entry_groups",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListEntryGroups",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListEntryTypes(
        _BaseCatalogServiceRestTransport._BaseListEntryTypes, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListEntryTypes")

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
            request: catalog.ListEntryTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.ListEntryTypesResponse:
            r"""Call the list entry types method over HTTP.

            Args:
                request (~.catalog.ListEntryTypesRequest):
                    The request object. List EntryTypes request
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.ListEntryTypesResponse:
                    List EntryTypes response.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListEntryTypes._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_entry_types(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListEntryTypes._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListEntryTypes._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.ListEntryTypes",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListEntryTypes",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListEntryTypes._get_response(
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
            resp = catalog.ListEntryTypesResponse()
            pb_resp = catalog.ListEntryTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_entry_types(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_entry_types_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.ListEntryTypesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.list_entry_types",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListEntryTypes",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListMetadataJobs(
        _BaseCatalogServiceRestTransport._BaseListMetadataJobs, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListMetadataJobs")

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
            request: catalog.ListMetadataJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.ListMetadataJobsResponse:
            r"""Call the list metadata jobs method over HTTP.

            Args:
                request (~.catalog.ListMetadataJobsRequest):
                    The request object. List metadata jobs request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.ListMetadataJobsResponse:
                    List metadata jobs response.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListMetadataJobs._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_metadata_jobs(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListMetadataJobs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListMetadataJobs._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.ListMetadataJobs",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListMetadataJobs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListMetadataJobs._get_response(
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
            resp = catalog.ListMetadataJobsResponse()
            pb_resp = catalog.ListMetadataJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_metadata_jobs(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_metadata_jobs_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.ListMetadataJobsResponse.to_json(
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.list_metadata_jobs",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListMetadataJobs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _LookupEntry(
        _BaseCatalogServiceRestTransport._BaseLookupEntry, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.LookupEntry")

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
            request: catalog.LookupEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.Entry:
            r"""Call the lookup entry method over HTTP.

            Args:
                request (~.catalog.LookupEntryRequest):
                    The request object. Lookup Entry request using
                permissions in the source system.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.Entry:
                    An entry is a representation of a
                data resource that can be described by
                various metadata.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseLookupEntry._get_http_options()
            )

            request, metadata = self._interceptor.pre_lookup_entry(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseLookupEntry._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseLookupEntry._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.LookupEntry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "LookupEntry",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._LookupEntry._get_response(
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
            resp = catalog.Entry()
            pb_resp = catalog.Entry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_lookup_entry(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_lookup_entry_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.Entry.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.lookup_entry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "LookupEntry",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SearchEntries(
        _BaseCatalogServiceRestTransport._BaseSearchEntries, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.SearchEntries")

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
            request: catalog.SearchEntriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.SearchEntriesResponse:
            r"""Call the search entries method over HTTP.

            Args:
                request (~.catalog.SearchEntriesRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.SearchEntriesResponse:

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseSearchEntries._get_http_options()
            )

            request, metadata = self._interceptor.pre_search_entries(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseSearchEntries._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseSearchEntries._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.SearchEntries",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "SearchEntries",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._SearchEntries._get_response(
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
            resp = catalog.SearchEntriesResponse()
            pb_resp = catalog.SearchEntriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_search_entries(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_search_entries_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.SearchEntriesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.search_entries",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "SearchEntries",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateAspectType(
        _BaseCatalogServiceRestTransport._BaseUpdateAspectType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.UpdateAspectType")

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
            request: catalog.UpdateAspectTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update aspect type method over HTTP.

            Args:
                request (~.catalog.UpdateAspectTypeRequest):
                    The request object. Update AspectType Request
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseUpdateAspectType._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_aspect_type(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseUpdateAspectType._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseUpdateAspectType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseUpdateAspectType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.UpdateAspectType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateAspectType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._UpdateAspectType._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_aspect_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_aspect_type_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.update_aspect_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateAspectType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateEntry(
        _BaseCatalogServiceRestTransport._BaseUpdateEntry, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.UpdateEntry")

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
            request: catalog.UpdateEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> catalog.Entry:
            r"""Call the update entry method over HTTP.

            Args:
                request (~.catalog.UpdateEntryRequest):
                    The request object. Update Entry request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.catalog.Entry:
                    An entry is a representation of a
                data resource that can be described by
                various metadata.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseUpdateEntry._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_entry(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseUpdateEntry._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseUpdateEntry._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseUpdateEntry._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.UpdateEntry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateEntry",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._UpdateEntry._get_response(
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
            resp = catalog.Entry()
            pb_resp = catalog.Entry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_entry(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_entry_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = catalog.Entry.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.update_entry",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateEntry",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateEntryGroup(
        _BaseCatalogServiceRestTransport._BaseUpdateEntryGroup, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.UpdateEntryGroup")

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
            request: catalog.UpdateEntryGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update entry group method over HTTP.

            Args:
                request (~.catalog.UpdateEntryGroupRequest):
                    The request object. Update EntryGroup Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseUpdateEntryGroup._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_entry_group(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseUpdateEntryGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseUpdateEntryGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseUpdateEntryGroup._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.UpdateEntryGroup",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateEntryGroup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._UpdateEntryGroup._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_entry_group(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_entry_group_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.update_entry_group",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateEntryGroup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateEntryType(
        _BaseCatalogServiceRestTransport._BaseUpdateEntryType, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.UpdateEntryType")

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
            request: catalog.UpdateEntryTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update entry type method over HTTP.

            Args:
                request (~.catalog.UpdateEntryTypeRequest):
                    The request object. Update EntryType Request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseUpdateEntryType._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_entry_type(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseUpdateEntryType._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseUpdateEntryType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseUpdateEntryType._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.UpdateEntryType",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateEntryType",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._UpdateEntryType._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_entry_type(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_entry_type_with_metadata(
                resp, response_metadata
            )
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceClient.update_entry_type",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "UpdateEntryType",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def cancel_metadata_job(
        self,
    ) -> Callable[[catalog.CancelMetadataJobRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelMetadataJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_aspect_type(
        self,
    ) -> Callable[[catalog.CreateAspectTypeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAspectType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_entry(self) -> Callable[[catalog.CreateEntryRequest], catalog.Entry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_entry_group(
        self,
    ) -> Callable[[catalog.CreateEntryGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEntryGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_entry_type(
        self,
    ) -> Callable[[catalog.CreateEntryTypeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEntryType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_metadata_job(
        self,
    ) -> Callable[[catalog.CreateMetadataJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMetadataJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_aspect_type(
        self,
    ) -> Callable[[catalog.DeleteAspectTypeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAspectType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_entry(self) -> Callable[[catalog.DeleteEntryRequest], catalog.Entry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_entry_group(
        self,
    ) -> Callable[[catalog.DeleteEntryGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEntryGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_entry_type(
        self,
    ) -> Callable[[catalog.DeleteEntryTypeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEntryType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_aspect_type(
        self,
    ) -> Callable[[catalog.GetAspectTypeRequest], catalog.AspectType]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAspectType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_entry(self) -> Callable[[catalog.GetEntryRequest], catalog.Entry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_entry_group(
        self,
    ) -> Callable[[catalog.GetEntryGroupRequest], catalog.EntryGroup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEntryGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_entry_type(
        self,
    ) -> Callable[[catalog.GetEntryTypeRequest], catalog.EntryType]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEntryType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_metadata_job(
        self,
    ) -> Callable[[catalog.GetMetadataJobRequest], catalog.MetadataJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMetadataJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_aspect_types(
        self,
    ) -> Callable[[catalog.ListAspectTypesRequest], catalog.ListAspectTypesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAspectTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_entries(
        self,
    ) -> Callable[[catalog.ListEntriesRequest], catalog.ListEntriesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEntries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_entry_groups(
        self,
    ) -> Callable[[catalog.ListEntryGroupsRequest], catalog.ListEntryGroupsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEntryGroups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_entry_types(
        self,
    ) -> Callable[[catalog.ListEntryTypesRequest], catalog.ListEntryTypesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEntryTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_metadata_jobs(
        self,
    ) -> Callable[[catalog.ListMetadataJobsRequest], catalog.ListMetadataJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMetadataJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lookup_entry(self) -> Callable[[catalog.LookupEntryRequest], catalog.Entry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LookupEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_entries(
        self,
    ) -> Callable[[catalog.SearchEntriesRequest], catalog.SearchEntriesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchEntries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_aspect_type(
        self,
    ) -> Callable[[catalog.UpdateAspectTypeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAspectType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_entry(self) -> Callable[[catalog.UpdateEntryRequest], catalog.Entry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_entry_group(
        self,
    ) -> Callable[[catalog.UpdateEntryGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEntryGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_entry_type(
        self,
    ) -> Callable[[catalog.UpdateEntryTypeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEntryType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseCatalogServiceRestTransport._BaseGetLocation, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetLocation")

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
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseGetLocation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetLocation._get_response(
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
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseCatalogServiceRestTransport._BaseListLocations, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListLocations")

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
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListLocations._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListLocations._get_response(
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
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseCatalogServiceRestTransport._BaseCancelOperation, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseCatalogServiceRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseCancelOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseCatalogServiceRestTransport._BaseDeleteOperation, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.DeleteOperation")

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
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseCatalogServiceRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseDeleteOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseCatalogServiceRestTransport._BaseGetOperation, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.GetOperation")

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
                _BaseCatalogServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseGetOperation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._GetOperation._get_response(
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseCatalogServiceRestTransport._BaseListOperations, CatalogServiceRestStub
    ):
        def __hash__(self):
            return hash("CatalogServiceRestTransport.ListOperations")

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
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseCatalogServiceRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseCatalogServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCatalogServiceRestTransport._BaseListOperations._get_query_params_json(
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
                    f"Sending request for google.cloud.dataplex_v1.CatalogServiceClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CatalogServiceRestTransport._ListOperations._get_response(
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
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
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
                    "Received response for google.cloud.dataplex_v1.CatalogServiceAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.dataplex.v1.CatalogService",
                        "rpcName": "ListOperations",
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


__all__ = ("CatalogServiceRestTransport",)
