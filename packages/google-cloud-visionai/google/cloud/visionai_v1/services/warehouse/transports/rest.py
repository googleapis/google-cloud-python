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

from google.cloud.visionai_v1.types import warehouse

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseWarehouseRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class WarehouseRestInterceptor:
    """Interceptor for Warehouse.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the WarehouseRestTransport.

    .. code-block:: python
        class MyCustomWarehouseInterceptor(WarehouseRestInterceptor):
            def pre_add_collection_item(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_collection_item(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_analyze_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_analyze_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_analyze_corpus(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_analyze_corpus(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_clip_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_clip_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_annotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_annotation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_collection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_collection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_corpus(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_corpus(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_data_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_data_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_index(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_index(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_index_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_index_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_search_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_search_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_search_hypernym(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_search_hypernym(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_annotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_collection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_collection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_corpus(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_data_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_index(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_index(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_index_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_index_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_search_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_search_hypernym(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_deploy_index(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_deploy_index(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_hls_uri(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_hls_uri(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_retrieval_url(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_retrieval_url(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_annotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_annotation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_collection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_collection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_corpus(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_corpus(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_index(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_index(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_index_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_index_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_search_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_search_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_search_hypernym(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_search_hypernym(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_index_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_index_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_annotations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_annotations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_collections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_collections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_corpora(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_corpora(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_data_schemas(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_schemas(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_index_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_index_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_indexes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_indexes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_search_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_search_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_search_hypernyms(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_search_hypernyms(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_collection_item(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_collection_item(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_index_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_index_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_index_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_index_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undeploy_index(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undeploy_index(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_annotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_annotation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_collection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_collection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_corpus(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_corpus(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_index(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_index(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_index_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_index_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_search_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_search_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_search_hypernym(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_search_hypernym(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_upload_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_upload_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_view_collection_items(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_view_collection_items(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_view_indexed_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_view_indexed_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = WarehouseRestTransport(interceptor=MyCustomWarehouseInterceptor())
        client = WarehouseClient(transport=transport)


    """

    def pre_add_collection_item(
        self,
        request: warehouse.AddCollectionItemRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.AddCollectionItemRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_collection_item

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_add_collection_item(
        self, response: warehouse.AddCollectionItemResponse
    ) -> warehouse.AddCollectionItemResponse:
        """Post-rpc interceptor for add_collection_item

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_analyze_asset(
        self,
        request: warehouse.AnalyzeAssetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.AnalyzeAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for analyze_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_analyze_asset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for analyze_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_analyze_corpus(
        self,
        request: warehouse.AnalyzeCorpusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.AnalyzeCorpusRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for analyze_corpus

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_analyze_corpus(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for analyze_corpus

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_clip_asset(
        self, request: warehouse.ClipAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.ClipAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for clip_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_clip_asset(
        self, response: warehouse.ClipAssetResponse
    ) -> warehouse.ClipAssetResponse:
        """Post-rpc interceptor for clip_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_annotation(
        self,
        request: warehouse.CreateAnnotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.CreateAnnotationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_annotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_annotation(
        self, response: warehouse.Annotation
    ) -> warehouse.Annotation:
        """Post-rpc interceptor for create_annotation

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_asset(
        self, request: warehouse.CreateAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.CreateAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_asset(self, response: warehouse.Asset) -> warehouse.Asset:
        """Post-rpc interceptor for create_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_collection(
        self,
        request: warehouse.CreateCollectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.CreateCollectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_collection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_collection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_collection

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_corpus(
        self,
        request: warehouse.CreateCorpusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.CreateCorpusRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_corpus

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_corpus(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_corpus

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_data_schema(
        self,
        request: warehouse.CreateDataSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.CreateDataSchemaRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_data_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_data_schema(
        self, response: warehouse.DataSchema
    ) -> warehouse.DataSchema:
        """Post-rpc interceptor for create_data_schema

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_index(
        self, request: warehouse.CreateIndexRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.CreateIndexRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_index

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_index(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_index

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_index_endpoint(
        self,
        request: warehouse.CreateIndexEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.CreateIndexEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_index_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_index_endpoint(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_index_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_search_config(
        self,
        request: warehouse.CreateSearchConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.CreateSearchConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_search_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_search_config(
        self, response: warehouse.SearchConfig
    ) -> warehouse.SearchConfig:
        """Post-rpc interceptor for create_search_config

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_create_search_hypernym(
        self,
        request: warehouse.CreateSearchHypernymRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.CreateSearchHypernymRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_search_hypernym

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_create_search_hypernym(
        self, response: warehouse.SearchHypernym
    ) -> warehouse.SearchHypernym:
        """Post-rpc interceptor for create_search_hypernym

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_delete_annotation(
        self,
        request: warehouse.DeleteAnnotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.DeleteAnnotationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_annotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def pre_delete_asset(
        self, request: warehouse.DeleteAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.DeleteAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_delete_asset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_delete_collection(
        self,
        request: warehouse.DeleteCollectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.DeleteCollectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_collection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_delete_collection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_collection

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_delete_corpus(
        self,
        request: warehouse.DeleteCorpusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.DeleteCorpusRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_corpus

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def pre_delete_data_schema(
        self,
        request: warehouse.DeleteDataSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.DeleteDataSchemaRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_data_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def pre_delete_index(
        self, request: warehouse.DeleteIndexRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.DeleteIndexRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_index

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_delete_index(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_index

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_delete_index_endpoint(
        self,
        request: warehouse.DeleteIndexEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.DeleteIndexEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_index_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_delete_index_endpoint(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_index_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_delete_search_config(
        self,
        request: warehouse.DeleteSearchConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.DeleteSearchConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_search_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def pre_delete_search_hypernym(
        self,
        request: warehouse.DeleteSearchHypernymRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.DeleteSearchHypernymRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_search_hypernym

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def pre_deploy_index(
        self, request: warehouse.DeployIndexRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.DeployIndexRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for deploy_index

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_deploy_index(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for deploy_index

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_generate_hls_uri(
        self,
        request: warehouse.GenerateHlsUriRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GenerateHlsUriRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for generate_hls_uri

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_generate_hls_uri(
        self, response: warehouse.GenerateHlsUriResponse
    ) -> warehouse.GenerateHlsUriResponse:
        """Post-rpc interceptor for generate_hls_uri

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_generate_retrieval_url(
        self,
        request: warehouse.GenerateRetrievalUrlRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GenerateRetrievalUrlRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for generate_retrieval_url

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_generate_retrieval_url(
        self, response: warehouse.GenerateRetrievalUrlResponse
    ) -> warehouse.GenerateRetrievalUrlResponse:
        """Post-rpc interceptor for generate_retrieval_url

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_annotation(
        self,
        request: warehouse.GetAnnotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GetAnnotationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_annotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_annotation(
        self, response: warehouse.Annotation
    ) -> warehouse.Annotation:
        """Post-rpc interceptor for get_annotation

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_asset(
        self, request: warehouse.GetAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.GetAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_asset(self, response: warehouse.Asset) -> warehouse.Asset:
        """Post-rpc interceptor for get_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_collection(
        self,
        request: warehouse.GetCollectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GetCollectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_collection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_collection(
        self, response: warehouse.Collection
    ) -> warehouse.Collection:
        """Post-rpc interceptor for get_collection

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_corpus(
        self, request: warehouse.GetCorpusRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.GetCorpusRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_corpus

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_corpus(self, response: warehouse.Corpus) -> warehouse.Corpus:
        """Post-rpc interceptor for get_corpus

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_data_schema(
        self,
        request: warehouse.GetDataSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GetDataSchemaRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_data_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_data_schema(
        self, response: warehouse.DataSchema
    ) -> warehouse.DataSchema:
        """Post-rpc interceptor for get_data_schema

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_index(
        self, request: warehouse.GetIndexRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.GetIndexRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_index

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_index(self, response: warehouse.Index) -> warehouse.Index:
        """Post-rpc interceptor for get_index

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_index_endpoint(
        self,
        request: warehouse.GetIndexEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GetIndexEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_index_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_index_endpoint(
        self, response: warehouse.IndexEndpoint
    ) -> warehouse.IndexEndpoint:
        """Post-rpc interceptor for get_index_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_search_config(
        self,
        request: warehouse.GetSearchConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GetSearchConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_search_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_search_config(
        self, response: warehouse.SearchConfig
    ) -> warehouse.SearchConfig:
        """Post-rpc interceptor for get_search_config

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_get_search_hypernym(
        self,
        request: warehouse.GetSearchHypernymRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.GetSearchHypernymRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_search_hypernym

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_search_hypernym(
        self, response: warehouse.SearchHypernym
    ) -> warehouse.SearchHypernym:
        """Post-rpc interceptor for get_search_hypernym

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_import_assets(
        self,
        request: warehouse.ImportAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ImportAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_import_assets(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_assets

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_index_asset(
        self, request: warehouse.IndexAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.IndexAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for index_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_index_asset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for index_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_annotations(
        self,
        request: warehouse.ListAnnotationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ListAnnotationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_annotations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_annotations(
        self, response: warehouse.ListAnnotationsResponse
    ) -> warehouse.ListAnnotationsResponse:
        """Post-rpc interceptor for list_annotations

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_assets(
        self, request: warehouse.ListAssetsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.ListAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_assets(
        self, response: warehouse.ListAssetsResponse
    ) -> warehouse.ListAssetsResponse:
        """Post-rpc interceptor for list_assets

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_collections(
        self,
        request: warehouse.ListCollectionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ListCollectionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_collections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_collections(
        self, response: warehouse.ListCollectionsResponse
    ) -> warehouse.ListCollectionsResponse:
        """Post-rpc interceptor for list_collections

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_corpora(
        self, request: warehouse.ListCorporaRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.ListCorporaRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_corpora

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_corpora(
        self, response: warehouse.ListCorporaResponse
    ) -> warehouse.ListCorporaResponse:
        """Post-rpc interceptor for list_corpora

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_data_schemas(
        self,
        request: warehouse.ListDataSchemasRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ListDataSchemasRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_data_schemas

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_data_schemas(
        self, response: warehouse.ListDataSchemasResponse
    ) -> warehouse.ListDataSchemasResponse:
        """Post-rpc interceptor for list_data_schemas

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_index_endpoints(
        self,
        request: warehouse.ListIndexEndpointsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ListIndexEndpointsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_index_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_index_endpoints(
        self, response: warehouse.ListIndexEndpointsResponse
    ) -> warehouse.ListIndexEndpointsResponse:
        """Post-rpc interceptor for list_index_endpoints

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_indexes(
        self, request: warehouse.ListIndexesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.ListIndexesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_indexes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_indexes(
        self, response: warehouse.ListIndexesResponse
    ) -> warehouse.ListIndexesResponse:
        """Post-rpc interceptor for list_indexes

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_search_configs(
        self,
        request: warehouse.ListSearchConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ListSearchConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_search_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_search_configs(
        self, response: warehouse.ListSearchConfigsResponse
    ) -> warehouse.ListSearchConfigsResponse:
        """Post-rpc interceptor for list_search_configs

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_list_search_hypernyms(
        self,
        request: warehouse.ListSearchHypernymsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ListSearchHypernymsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_search_hypernyms

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_search_hypernyms(
        self, response: warehouse.ListSearchHypernymsResponse
    ) -> warehouse.ListSearchHypernymsResponse:
        """Post-rpc interceptor for list_search_hypernyms

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_remove_collection_item(
        self,
        request: warehouse.RemoveCollectionItemRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.RemoveCollectionItemRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_collection_item

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_remove_collection_item(
        self, response: warehouse.RemoveCollectionItemResponse
    ) -> warehouse.RemoveCollectionItemResponse:
        """Post-rpc interceptor for remove_collection_item

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_remove_index_asset(
        self,
        request: warehouse.RemoveIndexAssetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.RemoveIndexAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_index_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_remove_index_asset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_index_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_search_assets(
        self,
        request: warehouse.SearchAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.SearchAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_search_assets(
        self, response: warehouse.SearchAssetsResponse
    ) -> warehouse.SearchAssetsResponse:
        """Post-rpc interceptor for search_assets

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_search_index_endpoint(
        self,
        request: warehouse.SearchIndexEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.SearchIndexEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_index_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_search_index_endpoint(
        self, response: warehouse.SearchIndexEndpointResponse
    ) -> warehouse.SearchIndexEndpointResponse:
        """Post-rpc interceptor for search_index_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_undeploy_index(
        self,
        request: warehouse.UndeployIndexRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UndeployIndexRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undeploy_index

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_undeploy_index(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undeploy_index

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_annotation(
        self,
        request: warehouse.UpdateAnnotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UpdateAnnotationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_annotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_annotation(
        self, response: warehouse.Annotation
    ) -> warehouse.Annotation:
        """Post-rpc interceptor for update_annotation

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_asset(
        self, request: warehouse.UpdateAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.UpdateAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_asset(self, response: warehouse.Asset) -> warehouse.Asset:
        """Post-rpc interceptor for update_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_collection(
        self,
        request: warehouse.UpdateCollectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UpdateCollectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_collection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_collection(
        self, response: warehouse.Collection
    ) -> warehouse.Collection:
        """Post-rpc interceptor for update_collection

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_corpus(
        self,
        request: warehouse.UpdateCorpusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UpdateCorpusRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_corpus

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_corpus(self, response: warehouse.Corpus) -> warehouse.Corpus:
        """Post-rpc interceptor for update_corpus

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_data_schema(
        self,
        request: warehouse.UpdateDataSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UpdateDataSchemaRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_data_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_data_schema(
        self, response: warehouse.DataSchema
    ) -> warehouse.DataSchema:
        """Post-rpc interceptor for update_data_schema

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_index(
        self, request: warehouse.UpdateIndexRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.UpdateIndexRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_index

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_index(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_index

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_index_endpoint(
        self,
        request: warehouse.UpdateIndexEndpointRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UpdateIndexEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_index_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_index_endpoint(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_index_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_search_config(
        self,
        request: warehouse.UpdateSearchConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UpdateSearchConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_search_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_search_config(
        self, response: warehouse.SearchConfig
    ) -> warehouse.SearchConfig:
        """Post-rpc interceptor for update_search_config

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_update_search_hypernym(
        self,
        request: warehouse.UpdateSearchHypernymRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.UpdateSearchHypernymRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_search_hypernym

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_update_search_hypernym(
        self, response: warehouse.SearchHypernym
    ) -> warehouse.SearchHypernym:
        """Post-rpc interceptor for update_search_hypernym

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_upload_asset(
        self, request: warehouse.UploadAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[warehouse.UploadAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for upload_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_upload_asset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for upload_asset

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_view_collection_items(
        self,
        request: warehouse.ViewCollectionItemsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ViewCollectionItemsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for view_collection_items

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_view_collection_items(
        self, response: warehouse.ViewCollectionItemsResponse
    ) -> warehouse.ViewCollectionItemsResponse:
        """Post-rpc interceptor for view_collection_items

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response

    def pre_view_indexed_assets(
        self,
        request: warehouse.ViewIndexedAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[warehouse.ViewIndexedAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for view_indexed_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_view_indexed_assets(
        self, response: warehouse.ViewIndexedAssetsResponse
    ) -> warehouse.ViewIndexedAssetsResponse:
        """Post-rpc interceptor for view_indexed_assets

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
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
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
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
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
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
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
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
        before they are sent to the Warehouse server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Warehouse server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class WarehouseRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: WarehouseRestInterceptor


class WarehouseRestTransport(_BaseWarehouseRestTransport):
    """REST backend synchronous transport for Warehouse.

    Service that manages media content + metadata for streaming.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "visionai.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[WarehouseRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'visionai.googleapis.com').
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
        self._interceptor = interceptor or WarehouseRestInterceptor()
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
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/warehouseOperations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/assets/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/collections/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/imageIndexes/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/indexes/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/corpora/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
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

    class _AddCollectionItem(
        _BaseWarehouseRestTransport._BaseAddCollectionItem, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.AddCollectionItem")

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
            request: warehouse.AddCollectionItemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.AddCollectionItemResponse:
            r"""Call the add collection item method over HTTP.

            Args:
                request (~.warehouse.AddCollectionItemRequest):
                    The request object. Request message for
                AddCollectionItem.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.AddCollectionItemResponse:
                    Response message for
                AddCollectionItem.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseAddCollectionItem._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_collection_item(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseAddCollectionItem._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseAddCollectionItem._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseAddCollectionItem._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._AddCollectionItem._get_response(
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
            resp = warehouse.AddCollectionItemResponse()
            pb_resp = warehouse.AddCollectionItemResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_collection_item(resp)
            return resp

    class _AnalyzeAsset(
        _BaseWarehouseRestTransport._BaseAnalyzeAsset, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.AnalyzeAsset")

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
            request: warehouse.AnalyzeAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the analyze asset method over HTTP.

            Args:
                request (~.warehouse.AnalyzeAssetRequest):
                    The request object. Request message for AnalyzeAsset.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseAnalyzeAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_analyze_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseAnalyzeAsset._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseAnalyzeAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseAnalyzeAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._AnalyzeAsset._get_response(
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
            resp = self._interceptor.post_analyze_asset(resp)
            return resp

    class _AnalyzeCorpus(
        _BaseWarehouseRestTransport._BaseAnalyzeCorpus, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.AnalyzeCorpus")

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
            request: warehouse.AnalyzeCorpusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the analyze corpus method over HTTP.

            Args:
                request (~.warehouse.AnalyzeCorpusRequest):
                    The request object. Request message for AnalyzeCorpus.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseAnalyzeCorpus._get_http_options()
            )
            request, metadata = self._interceptor.pre_analyze_corpus(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseAnalyzeCorpus._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseWarehouseRestTransport._BaseAnalyzeCorpus._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseAnalyzeCorpus._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._AnalyzeCorpus._get_response(
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
            resp = self._interceptor.post_analyze_corpus(resp)
            return resp

    class _ClipAsset(_BaseWarehouseRestTransport._BaseClipAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.ClipAsset")

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
            request: warehouse.ClipAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ClipAssetResponse:
            r"""Call the clip asset method over HTTP.

            Args:
                request (~.warehouse.ClipAssetRequest):
                    The request object. Request message for ClipAsset API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ClipAssetResponse:
                    Response message for ClipAsset API.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseClipAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_clip_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseClipAsset._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseClipAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseClipAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ClipAsset._get_response(
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
            resp = warehouse.ClipAssetResponse()
            pb_resp = warehouse.ClipAssetResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_clip_asset(resp)
            return resp

    class _CreateAnnotation(
        _BaseWarehouseRestTransport._BaseCreateAnnotation, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateAnnotation")

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
            request: warehouse.CreateAnnotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Annotation:
            r"""Call the create annotation method over HTTP.

            Args:
                request (~.warehouse.CreateAnnotationRequest):
                    The request object. Request message for CreateAnnotation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Annotation:
                    An annotation is a resource in asset.
                It represents a key-value mapping of
                content in asset.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateAnnotation._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_annotation(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseCreateAnnotation._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseCreateAnnotation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseCreateAnnotation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._CreateAnnotation._get_response(
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
            resp = warehouse.Annotation()
            pb_resp = warehouse.Annotation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_annotation(resp)
            return resp

    class _CreateAsset(_BaseWarehouseRestTransport._BaseCreateAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateAsset")

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
            request: warehouse.CreateAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Asset:
            r"""Call the create asset method over HTTP.

            Args:
                request (~.warehouse.CreateAssetRequest):
                    The request object. Request message for
                CreateAssetRequest.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Asset:
                    An asset is a resource in corpus. It
                represents a media object inside corpus,
                contains metadata and another resource
                annotation. Different feature could be
                applied to the asset to generate
                annotations. User could specified
                annotation related to the target asset.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseCreateAsset._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseCreateAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseCreateAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._CreateAsset._get_response(
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
            resp = warehouse.Asset()
            pb_resp = warehouse.Asset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_asset(resp)
            return resp

    class _CreateCollection(
        _BaseWarehouseRestTransport._BaseCreateCollection, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateCollection")

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
            request: warehouse.CreateCollectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create collection method over HTTP.

            Args:
                request (~.warehouse.CreateCollectionRequest):
                    The request object. Request message for CreateCollection.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateCollection._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_collection(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseCreateCollection._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseCreateCollection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseCreateCollection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._CreateCollection._get_response(
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
            resp = self._interceptor.post_create_collection(resp)
            return resp

    class _CreateCorpus(
        _BaseWarehouseRestTransport._BaseCreateCorpus, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateCorpus")

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
            request: warehouse.CreateCorpusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create corpus method over HTTP.

            Args:
                request (~.warehouse.CreateCorpusRequest):
                    The request object. Request message of CreateCorpus API.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateCorpus._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_corpus(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseCreateCorpus._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseCreateCorpus._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseCreateCorpus._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._CreateCorpus._get_response(
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
            resp = self._interceptor.post_create_corpus(resp)
            return resp

    class _CreateDataSchema(
        _BaseWarehouseRestTransport._BaseCreateDataSchema, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateDataSchema")

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
            request: warehouse.CreateDataSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.DataSchema:
            r"""Call the create data schema method over HTTP.

            Args:
                request (~.warehouse.CreateDataSchemaRequest):
                    The request object. Request message for CreateDataSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.DataSchema:
                    Data schema indicates how the user
                specified annotation is interpreted in
                the system.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateDataSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_data_schema(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseCreateDataSchema._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseCreateDataSchema._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseCreateDataSchema._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._CreateDataSchema._get_response(
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
            resp = warehouse.DataSchema()
            pb_resp = warehouse.DataSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_data_schema(resp)
            return resp

    class _CreateIndex(_BaseWarehouseRestTransport._BaseCreateIndex, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateIndex")

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
            request: warehouse.CreateIndexRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create index method over HTTP.

            Args:
                request (~.warehouse.CreateIndexRequest):
                    The request object. Message for creating an Index.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateIndex._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_index(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseCreateIndex._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseCreateIndex._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseCreateIndex._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._CreateIndex._get_response(
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
            resp = self._interceptor.post_create_index(resp)
            return resp

    class _CreateIndexEndpoint(
        _BaseWarehouseRestTransport._BaseCreateIndexEndpoint, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateIndexEndpoint")

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
            request: warehouse.CreateIndexEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create index endpoint method over HTTP.

            Args:
                request (~.warehouse.CreateIndexEndpointRequest):
                    The request object. Request message for
                CreateIndexEndpoint.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateIndexEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_index_endpoint(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseCreateIndexEndpoint._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseCreateIndexEndpoint._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseCreateIndexEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._CreateIndexEndpoint._get_response(
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
            resp = self._interceptor.post_create_index_endpoint(resp)
            return resp

    class _CreateSearchConfig(
        _BaseWarehouseRestTransport._BaseCreateSearchConfig, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateSearchConfig")

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
            request: warehouse.CreateSearchConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchConfig:
            r"""Call the create search config method over HTTP.

            Args:
                request (~.warehouse.CreateSearchConfigRequest):
                    The request object. Request message for
                CreateSearchConfig.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchConfig:
                    SearchConfig stores different
                properties that will affect search
                behaviors and search results.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateSearchConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_search_config(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseCreateSearchConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseCreateSearchConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseCreateSearchConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._CreateSearchConfig._get_response(
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
            resp = warehouse.SearchConfig()
            pb_resp = warehouse.SearchConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_search_config(resp)
            return resp

    class _CreateSearchHypernym(
        _BaseWarehouseRestTransport._BaseCreateSearchHypernym, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CreateSearchHypernym")

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
            request: warehouse.CreateSearchHypernymRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchHypernym:
            r"""Call the create search hypernym method over HTTP.

            Args:
                request (~.warehouse.CreateSearchHypernymRequest):
                    The request object. Request message for creating
                SearchHypernym.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchHypernym:
                    Search resource: SearchHypernym. For example, {
                hypernym: "vehicle" hyponyms: ["sedan", "truck"] } This
                means in SMART_SEARCH mode, searching for "vehicle" will
                also return results with "sedan" or "truck" as
                annotations.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseCreateSearchHypernym._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_search_hypernym(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseCreateSearchHypernym._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseCreateSearchHypernym._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseCreateSearchHypernym._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._CreateSearchHypernym._get_response(
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
            resp = warehouse.SearchHypernym()
            pb_resp = warehouse.SearchHypernym.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_search_hypernym(resp)
            return resp

    class _DeleteAnnotation(
        _BaseWarehouseRestTransport._BaseDeleteAnnotation, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteAnnotation")

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
            request: warehouse.DeleteAnnotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete annotation method over HTTP.

            Args:
                request (~.warehouse.DeleteAnnotationRequest):
                    The request object. Request message for DeleteAnnotation
                API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteAnnotation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_annotation(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseDeleteAnnotation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseDeleteAnnotation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._DeleteAnnotation._get_response(
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

    class _DeleteAsset(_BaseWarehouseRestTransport._BaseDeleteAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteAsset")

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
            request: warehouse.DeleteAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete asset method over HTTP.

            Args:
                request (~.warehouse.DeleteAssetRequest):
                    The request object. Request message for DeleteAsset.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseDeleteAsset._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseDeleteAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._DeleteAsset._get_response(
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
            resp = self._interceptor.post_delete_asset(resp)
            return resp

    class _DeleteCollection(
        _BaseWarehouseRestTransport._BaseDeleteCollection, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteCollection")

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
            request: warehouse.DeleteCollectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete collection method over HTTP.

            Args:
                request (~.warehouse.DeleteCollectionRequest):
                    The request object. Request message for
                DeleteCollectionRequest.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteCollection._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_collection(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseDeleteCollection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseDeleteCollection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._DeleteCollection._get_response(
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
            resp = self._interceptor.post_delete_collection(resp)
            return resp

    class _DeleteCorpus(
        _BaseWarehouseRestTransport._BaseDeleteCorpus, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteCorpus")

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
            request: warehouse.DeleteCorpusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete corpus method over HTTP.

            Args:
                request (~.warehouse.DeleteCorpusRequest):
                    The request object. Request message for DeleteCorpus.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteCorpus._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_corpus(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseDeleteCorpus._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseDeleteCorpus._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._DeleteCorpus._get_response(
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

    class _DeleteDataSchema(
        _BaseWarehouseRestTransport._BaseDeleteDataSchema, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteDataSchema")

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
            request: warehouse.DeleteDataSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete data schema method over HTTP.

            Args:
                request (~.warehouse.DeleteDataSchemaRequest):
                    The request object. Request message for DeleteDataSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteDataSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_data_schema(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseDeleteDataSchema._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseDeleteDataSchema._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._DeleteDataSchema._get_response(
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

    class _DeleteIndex(_BaseWarehouseRestTransport._BaseDeleteIndex, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteIndex")

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
            request: warehouse.DeleteIndexRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete index method over HTTP.

            Args:
                request (~.warehouse.DeleteIndexRequest):
                    The request object. Request message for DeleteIndex.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteIndex._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_index(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseDeleteIndex._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseDeleteIndex._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._DeleteIndex._get_response(
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
            resp = self._interceptor.post_delete_index(resp)
            return resp

    class _DeleteIndexEndpoint(
        _BaseWarehouseRestTransport._BaseDeleteIndexEndpoint, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteIndexEndpoint")

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
            request: warehouse.DeleteIndexEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete index endpoint method over HTTP.

            Args:
                request (~.warehouse.DeleteIndexEndpointRequest):
                    The request object. Request message for
                DeleteIndexEndpoint.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteIndexEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_index_endpoint(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseDeleteIndexEndpoint._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseDeleteIndexEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._DeleteIndexEndpoint._get_response(
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
            resp = self._interceptor.post_delete_index_endpoint(resp)
            return resp

    class _DeleteSearchConfig(
        _BaseWarehouseRestTransport._BaseDeleteSearchConfig, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteSearchConfig")

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
            request: warehouse.DeleteSearchConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete search config method over HTTP.

            Args:
                request (~.warehouse.DeleteSearchConfigRequest):
                    The request object. Request message for
                DeleteSearchConfig.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteSearchConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_search_config(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseDeleteSearchConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseDeleteSearchConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._DeleteSearchConfig._get_response(
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

    class _DeleteSearchHypernym(
        _BaseWarehouseRestTransport._BaseDeleteSearchHypernym, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteSearchHypernym")

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
            request: warehouse.DeleteSearchHypernymRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete search hypernym method over HTTP.

            Args:
                request (~.warehouse.DeleteSearchHypernymRequest):
                    The request object. Request message for deleting
                SearchHypernym.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteSearchHypernym._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_search_hypernym(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseDeleteSearchHypernym._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseDeleteSearchHypernym._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._DeleteSearchHypernym._get_response(
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

    class _DeployIndex(_BaseWarehouseRestTransport._BaseDeployIndex, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeployIndex")

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
            request: warehouse.DeployIndexRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the deploy index method over HTTP.

            Args:
                request (~.warehouse.DeployIndexRequest):
                    The request object. Request message for DeployIndex.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseDeployIndex._get_http_options()
            )
            request, metadata = self._interceptor.pre_deploy_index(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseDeployIndex._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseDeployIndex._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseDeployIndex._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._DeployIndex._get_response(
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
            resp = self._interceptor.post_deploy_index(resp)
            return resp

    class _GenerateHlsUri(
        _BaseWarehouseRestTransport._BaseGenerateHlsUri, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GenerateHlsUri")

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
            request: warehouse.GenerateHlsUriRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.GenerateHlsUriResponse:
            r"""Call the generate hls uri method over HTTP.

            Args:
                request (~.warehouse.GenerateHlsUriRequest):
                    The request object. Request message for GenerateHlsUri
                API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.GenerateHlsUriResponse:
                    Response message for GenerateHlsUri
                API.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGenerateHlsUri._get_http_options()
            )
            request, metadata = self._interceptor.pre_generate_hls_uri(
                request, metadata
            )
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGenerateHlsUri._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseWarehouseRestTransport._BaseGenerateHlsUri._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGenerateHlsUri._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GenerateHlsUri._get_response(
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
            resp = warehouse.GenerateHlsUriResponse()
            pb_resp = warehouse.GenerateHlsUriResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_hls_uri(resp)
            return resp

    class _GenerateRetrievalUrl(
        _BaseWarehouseRestTransport._BaseGenerateRetrievalUrl, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GenerateRetrievalUrl")

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
            request: warehouse.GenerateRetrievalUrlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.GenerateRetrievalUrlResponse:
            r"""Call the generate retrieval url method over HTTP.

            Args:
                request (~.warehouse.GenerateRetrievalUrlRequest):
                    The request object. Request message for
                GenerateRetrievalUrl API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.GenerateRetrievalUrlResponse:
                    Response message for
                GenerateRetrievalUrl API.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGenerateRetrievalUrl._get_http_options()
            )
            request, metadata = self._interceptor.pre_generate_retrieval_url(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseGenerateRetrievalUrl._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseGenerateRetrievalUrl._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseGenerateRetrievalUrl._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._GenerateRetrievalUrl._get_response(
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
            resp = warehouse.GenerateRetrievalUrlResponse()
            pb_resp = warehouse.GenerateRetrievalUrlResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_retrieval_url(resp)
            return resp

    class _GetAnnotation(
        _BaseWarehouseRestTransport._BaseGetAnnotation, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetAnnotation")

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
            request: warehouse.GetAnnotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Annotation:
            r"""Call the get annotation method over HTTP.

            Args:
                request (~.warehouse.GetAnnotationRequest):
                    The request object. Request message for GetAnnotation
                API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Annotation:
                    An annotation is a resource in asset.
                It represents a key-value mapping of
                content in asset.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGetAnnotation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_annotation(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGetAnnotation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetAnnotation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetAnnotation._get_response(
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
            resp = warehouse.Annotation()
            pb_resp = warehouse.Annotation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_annotation(resp)
            return resp

    class _GetAsset(_BaseWarehouseRestTransport._BaseGetAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetAsset")

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
            request: warehouse.GetAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Asset:
            r"""Call the get asset method over HTTP.

            Args:
                request (~.warehouse.GetAssetRequest):
                    The request object. Request message for GetAsset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Asset:
                    An asset is a resource in corpus. It
                represents a media object inside corpus,
                contains metadata and another resource
                annotation. Different feature could be
                applied to the asset to generate
                annotations. User could specified
                annotation related to the target asset.

            """

            http_options = _BaseWarehouseRestTransport._BaseGetAsset._get_http_options()
            request, metadata = self._interceptor.pre_get_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGetAsset._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetAsset._get_response(
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
            resp = warehouse.Asset()
            pb_resp = warehouse.Asset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_asset(resp)
            return resp

    class _GetCollection(
        _BaseWarehouseRestTransport._BaseGetCollection, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetCollection")

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
            request: warehouse.GetCollectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Collection:
            r"""Call the get collection method over HTTP.

            Args:
                request (~.warehouse.GetCollectionRequest):
                    The request object. Request message for
                GetCollectionRequest.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Collection:
                    A collection is a resource in a
                corpus. It serves as a container of
                references to original resources.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGetCollection._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_collection(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGetCollection._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetCollection._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetCollection._get_response(
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
            resp = warehouse.Collection()
            pb_resp = warehouse.Collection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_collection(resp)
            return resp

    class _GetCorpus(_BaseWarehouseRestTransport._BaseGetCorpus, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetCorpus")

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
            request: warehouse.GetCorpusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Corpus:
            r"""Call the get corpus method over HTTP.

            Args:
                request (~.warehouse.GetCorpusRequest):
                    The request object. Request message for GetCorpus.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Corpus:
                    Corpus is a set of media contents for
                management. Within a corpus, media
                shares the same data schema. Search is
                also restricted within a single corpus.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGetCorpus._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_corpus(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGetCorpus._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetCorpus._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetCorpus._get_response(
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
            resp = warehouse.Corpus()
            pb_resp = warehouse.Corpus.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_corpus(resp)
            return resp

    class _GetDataSchema(
        _BaseWarehouseRestTransport._BaseGetDataSchema, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetDataSchema")

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
            request: warehouse.GetDataSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.DataSchema:
            r"""Call the get data schema method over HTTP.

            Args:
                request (~.warehouse.GetDataSchemaRequest):
                    The request object. Request message for GetDataSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.DataSchema:
                    Data schema indicates how the user
                specified annotation is interpreted in
                the system.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGetDataSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_data_schema(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGetDataSchema._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetDataSchema._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetDataSchema._get_response(
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
            resp = warehouse.DataSchema()
            pb_resp = warehouse.DataSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_schema(resp)
            return resp

    class _GetIndex(_BaseWarehouseRestTransport._BaseGetIndex, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetIndex")

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
            request: warehouse.GetIndexRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Index:
            r"""Call the get index method over HTTP.

            Args:
                request (~.warehouse.GetIndexRequest):
                    The request object. Request message for getting an Index.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Index:
                    An Index is a resource in Corpus. It
                contains an indexed version of the
                assets and annotations. When deployed to
                an endpoint, it will allow users to
                search the Index.

            """

            http_options = _BaseWarehouseRestTransport._BaseGetIndex._get_http_options()
            request, metadata = self._interceptor.pre_get_index(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGetIndex._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetIndex._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetIndex._get_response(
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
            resp = warehouse.Index()
            pb_resp = warehouse.Index.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_index(resp)
            return resp

    class _GetIndexEndpoint(
        _BaseWarehouseRestTransport._BaseGetIndexEndpoint, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetIndexEndpoint")

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
            request: warehouse.GetIndexEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.IndexEndpoint:
            r"""Call the get index endpoint method over HTTP.

            Args:
                request (~.warehouse.GetIndexEndpointRequest):
                    The request object. Request message for GetIndexEndpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.IndexEndpoint:
                    Message representing IndexEndpoint
                resource. Indexes are deployed into it.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGetIndexEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_index_endpoint(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseGetIndexEndpoint._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseGetIndexEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._GetIndexEndpoint._get_response(
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
            resp = warehouse.IndexEndpoint()
            pb_resp = warehouse.IndexEndpoint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_index_endpoint(resp)
            return resp

    class _GetSearchConfig(
        _BaseWarehouseRestTransport._BaseGetSearchConfig, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetSearchConfig")

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
            request: warehouse.GetSearchConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchConfig:
            r"""Call the get search config method over HTTP.

            Args:
                request (~.warehouse.GetSearchConfigRequest):
                    The request object. Request message for GetSearchConfig.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchConfig:
                    SearchConfig stores different
                properties that will affect search
                behaviors and search results.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGetSearchConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_search_config(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseGetSearchConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetSearchConfig._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetSearchConfig._get_response(
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
            resp = warehouse.SearchConfig()
            pb_resp = warehouse.SearchConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_search_config(resp)
            return resp

    class _GetSearchHypernym(
        _BaseWarehouseRestTransport._BaseGetSearchHypernym, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetSearchHypernym")

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
            request: warehouse.GetSearchHypernymRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchHypernym:
            r"""Call the get search hypernym method over HTTP.

            Args:
                request (~.warehouse.GetSearchHypernymRequest):
                    The request object. Request message for getting
                SearchHypernym.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchHypernym:
                    Search resource: SearchHypernym. For example, {
                hypernym: "vehicle" hyponyms: ["sedan", "truck"] } This
                means in SMART_SEARCH mode, searching for "vehicle" will
                also return results with "sedan" or "truck" as
                annotations.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseGetSearchHypernym._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_search_hypernym(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseGetSearchHypernym._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseGetSearchHypernym._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._GetSearchHypernym._get_response(
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
            resp = warehouse.SearchHypernym()
            pb_resp = warehouse.SearchHypernym.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_search_hypernym(resp)
            return resp

    class _ImportAssets(
        _BaseWarehouseRestTransport._BaseImportAssets, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ImportAssets")

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
            request: warehouse.ImportAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import assets method over HTTP.

            Args:
                request (~.warehouse.ImportAssetsRequest):
                    The request object. The request message for ImportAssets.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseImportAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_import_assets(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseImportAssets._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseImportAssets._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseImportAssets._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ImportAssets._get_response(
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
            resp = self._interceptor.post_import_assets(resp)
            return resp

    class _IndexAsset(_BaseWarehouseRestTransport._BaseIndexAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.IndexAsset")

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
            request: warehouse.IndexAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the index asset method over HTTP.

            Args:
                request (~.warehouse.IndexAssetRequest):
                    The request object. Request message for IndexAsset.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseIndexAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_index_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseIndexAsset._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseIndexAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseIndexAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._IndexAsset._get_response(
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
            resp = self._interceptor.post_index_asset(resp)
            return resp

    class _IngestAsset(_BaseWarehouseRestTransport._BaseIngestAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.IngestAsset")

        def __call__(
            self,
            request: warehouse.IngestAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method IngestAsset is not available over REST transport"
            )

    class _ListAnnotations(
        _BaseWarehouseRestTransport._BaseListAnnotations, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListAnnotations")

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
            request: warehouse.ListAnnotationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListAnnotationsResponse:
            r"""Call the list annotations method over HTTP.

            Args:
                request (~.warehouse.ListAnnotationsRequest):
                    The request object. Request message for GetAnnotation
                API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListAnnotationsResponse:
                    Request message for ListAnnotations
                API.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListAnnotations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_annotations(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseListAnnotations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseListAnnotations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ListAnnotations._get_response(
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
            resp = warehouse.ListAnnotationsResponse()
            pb_resp = warehouse.ListAnnotationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_annotations(resp)
            return resp

    class _ListAssets(_BaseWarehouseRestTransport._BaseListAssets, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListAssets")

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
            request: warehouse.ListAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListAssetsResponse:
            r"""Call the list assets method over HTTP.

            Args:
                request (~.warehouse.ListAssetsRequest):
                    The request object. Request message for ListAssets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListAssetsResponse:
                    Response message for ListAssets.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_assets(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseListAssets._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseListAssets._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ListAssets._get_response(
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
            resp = warehouse.ListAssetsResponse()
            pb_resp = warehouse.ListAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_assets(resp)
            return resp

    class _ListCollections(
        _BaseWarehouseRestTransport._BaseListCollections, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListCollections")

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
            request: warehouse.ListCollectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListCollectionsResponse:
            r"""Call the list collections method over HTTP.

            Args:
                request (~.warehouse.ListCollectionsRequest):
                    The request object. Request message for ListCollections.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListCollectionsResponse:
                    Response message for ListCollections.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListCollections._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_collections(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseListCollections._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseListCollections._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ListCollections._get_response(
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
            resp = warehouse.ListCollectionsResponse()
            pb_resp = warehouse.ListCollectionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_collections(resp)
            return resp

    class _ListCorpora(_BaseWarehouseRestTransport._BaseListCorpora, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListCorpora")

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
            request: warehouse.ListCorporaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListCorporaResponse:
            r"""Call the list corpora method over HTTP.

            Args:
                request (~.warehouse.ListCorporaRequest):
                    The request object. Request message for ListCorpora.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListCorporaResponse:
                    Response message for ListCorpora.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListCorpora._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_corpora(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseListCorpora._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseListCorpora._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ListCorpora._get_response(
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
            resp = warehouse.ListCorporaResponse()
            pb_resp = warehouse.ListCorporaResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_corpora(resp)
            return resp

    class _ListDataSchemas(
        _BaseWarehouseRestTransport._BaseListDataSchemas, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListDataSchemas")

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
            request: warehouse.ListDataSchemasRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListDataSchemasResponse:
            r"""Call the list data schemas method over HTTP.

            Args:
                request (~.warehouse.ListDataSchemasRequest):
                    The request object. Request message for ListDataSchemas.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListDataSchemasResponse:
                    Response message for ListDataSchemas.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListDataSchemas._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_data_schemas(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseListDataSchemas._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseListDataSchemas._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ListDataSchemas._get_response(
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
            resp = warehouse.ListDataSchemasResponse()
            pb_resp = warehouse.ListDataSchemasResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_data_schemas(resp)
            return resp

    class _ListIndexEndpoints(
        _BaseWarehouseRestTransport._BaseListIndexEndpoints, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListIndexEndpoints")

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
            request: warehouse.ListIndexEndpointsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListIndexEndpointsResponse:
            r"""Call the list index endpoints method over HTTP.

            Args:
                request (~.warehouse.ListIndexEndpointsRequest):
                    The request object. Request message for
                ListIndexEndpoints.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListIndexEndpointsResponse:
                    Response message for
                ListIndexEndpoints.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListIndexEndpoints._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_index_endpoints(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseListIndexEndpoints._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseListIndexEndpoints._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._ListIndexEndpoints._get_response(
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
            resp = warehouse.ListIndexEndpointsResponse()
            pb_resp = warehouse.ListIndexEndpointsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_index_endpoints(resp)
            return resp

    class _ListIndexes(_BaseWarehouseRestTransport._BaseListIndexes, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListIndexes")

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
            request: warehouse.ListIndexesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListIndexesResponse:
            r"""Call the list indexes method over HTTP.

            Args:
                request (~.warehouse.ListIndexesRequest):
                    The request object. Request message for listing Indexes.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListIndexesResponse:
                    Response message for ListIndexes.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListIndexes._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_indexes(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseListIndexes._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseListIndexes._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ListIndexes._get_response(
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
            resp = warehouse.ListIndexesResponse()
            pb_resp = warehouse.ListIndexesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_indexes(resp)
            return resp

    class _ListSearchConfigs(
        _BaseWarehouseRestTransport._BaseListSearchConfigs, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListSearchConfigs")

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
            request: warehouse.ListSearchConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListSearchConfigsResponse:
            r"""Call the list search configs method over HTTP.

            Args:
                request (~.warehouse.ListSearchConfigsRequest):
                    The request object. Request message for
                ListSearchConfigs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListSearchConfigsResponse:
                    Response message for
                ListSearchConfigs.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListSearchConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_search_configs(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseListSearchConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseListSearchConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._ListSearchConfigs._get_response(
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
            resp = warehouse.ListSearchConfigsResponse()
            pb_resp = warehouse.ListSearchConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_search_configs(resp)
            return resp

    class _ListSearchHypernyms(
        _BaseWarehouseRestTransport._BaseListSearchHypernyms, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListSearchHypernyms")

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
            request: warehouse.ListSearchHypernymsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ListSearchHypernymsResponse:
            r"""Call the list search hypernyms method over HTTP.

            Args:
                request (~.warehouse.ListSearchHypernymsRequest):
                    The request object. Request message for listing
                SearchHypernyms.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ListSearchHypernymsResponse:
                    Response message for listing
                SearchHypernyms.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseListSearchHypernyms._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_search_hypernyms(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseListSearchHypernyms._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseListSearchHypernyms._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._ListSearchHypernyms._get_response(
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
            resp = warehouse.ListSearchHypernymsResponse()
            pb_resp = warehouse.ListSearchHypernymsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_search_hypernyms(resp)
            return resp

    class _RemoveCollectionItem(
        _BaseWarehouseRestTransport._BaseRemoveCollectionItem, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.RemoveCollectionItem")

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
            request: warehouse.RemoveCollectionItemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.RemoveCollectionItemResponse:
            r"""Call the remove collection item method over HTTP.

            Args:
                request (~.warehouse.RemoveCollectionItemRequest):
                    The request object. Request message for
                RemoveCollectionItem.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.RemoveCollectionItemResponse:
                    Request message for
                RemoveCollectionItem.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseRemoveCollectionItem._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_collection_item(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseRemoveCollectionItem._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseRemoveCollectionItem._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseRemoveCollectionItem._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._RemoveCollectionItem._get_response(
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
            resp = warehouse.RemoveCollectionItemResponse()
            pb_resp = warehouse.RemoveCollectionItemResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_remove_collection_item(resp)
            return resp

    class _RemoveIndexAsset(
        _BaseWarehouseRestTransport._BaseRemoveIndexAsset, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.RemoveIndexAsset")

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
            request: warehouse.RemoveIndexAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove index asset method over HTTP.

            Args:
                request (~.warehouse.RemoveIndexAssetRequest):
                    The request object. Request message for RemoveIndexAsset.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseRemoveIndexAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_index_asset(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseRemoveIndexAsset._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseRemoveIndexAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseRemoveIndexAsset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._RemoveIndexAsset._get_response(
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
            resp = self._interceptor.post_remove_index_asset(resp)
            return resp

    class _SearchAssets(
        _BaseWarehouseRestTransport._BaseSearchAssets, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.SearchAssets")

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
            request: warehouse.SearchAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchAssetsResponse:
            r"""Call the search assets method over HTTP.

            Args:
                request (~.warehouse.SearchAssetsRequest):
                    The request object. Request message for SearchAssets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchAssetsResponse:
                    Response message for SearchAssets.
            """

            http_options = (
                _BaseWarehouseRestTransport._BaseSearchAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_search_assets(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseSearchAssets._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseSearchAssets._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseSearchAssets._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._SearchAssets._get_response(
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
            resp = warehouse.SearchAssetsResponse()
            pb_resp = warehouse.SearchAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_assets(resp)
            return resp

    class _SearchIndexEndpoint(
        _BaseWarehouseRestTransport._BaseSearchIndexEndpoint, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.SearchIndexEndpoint")

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
            request: warehouse.SearchIndexEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchIndexEndpointResponse:
            r"""Call the search index endpoint method over HTTP.

            Args:
                request (~.warehouse.SearchIndexEndpointRequest):
                    The request object. Request message for
                SearchIndexEndpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchIndexEndpointResponse:
                    Response message for
                SearchIndexEndpoint.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseSearchIndexEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_search_index_endpoint(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseSearchIndexEndpoint._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseSearchIndexEndpoint._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseSearchIndexEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._SearchIndexEndpoint._get_response(
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
            resp = warehouse.SearchIndexEndpointResponse()
            pb_resp = warehouse.SearchIndexEndpointResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_index_endpoint(resp)
            return resp

    class _UndeployIndex(
        _BaseWarehouseRestTransport._BaseUndeployIndex, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UndeployIndex")

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
            request: warehouse.UndeployIndexRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undeploy index method over HTTP.

            Args:
                request (~.warehouse.UndeployIndexRequest):
                    The request object. Request message for
                UndeployIndexEndpoint.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseUndeployIndex._get_http_options()
            )
            request, metadata = self._interceptor.pre_undeploy_index(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseUndeployIndex._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseWarehouseRestTransport._BaseUndeployIndex._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseUndeployIndex._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._UndeployIndex._get_response(
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
            resp = self._interceptor.post_undeploy_index(resp)
            return resp

    class _UpdateAnnotation(
        _BaseWarehouseRestTransport._BaseUpdateAnnotation, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateAnnotation")

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
            request: warehouse.UpdateAnnotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Annotation:
            r"""Call the update annotation method over HTTP.

            Args:
                request (~.warehouse.UpdateAnnotationRequest):
                    The request object. Request message for UpdateAnnotation
                API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Annotation:
                    An annotation is a resource in asset.
                It represents a key-value mapping of
                content in asset.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateAnnotation._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_annotation(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseUpdateAnnotation._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseUpdateAnnotation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseUpdateAnnotation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._UpdateAnnotation._get_response(
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
            resp = warehouse.Annotation()
            pb_resp = warehouse.Annotation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_annotation(resp)
            return resp

    class _UpdateAsset(_BaseWarehouseRestTransport._BaseUpdateAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateAsset")

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
            request: warehouse.UpdateAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Asset:
            r"""Call the update asset method over HTTP.

            Args:
                request (~.warehouse.UpdateAssetRequest):
                    The request object. Request message for UpdateAsset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Asset:
                    An asset is a resource in corpus. It
                represents a media object inside corpus,
                contains metadata and another resource
                annotation. Different feature could be
                applied to the asset to generate
                annotations. User could specified
                annotation related to the target asset.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseUpdateAsset._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseUpdateAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseUpdateAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._UpdateAsset._get_response(
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
            resp = warehouse.Asset()
            pb_resp = warehouse.Asset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_asset(resp)
            return resp

    class _UpdateCollection(
        _BaseWarehouseRestTransport._BaseUpdateCollection, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateCollection")

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
            request: warehouse.UpdateCollectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Collection:
            r"""Call the update collection method over HTTP.

            Args:
                request (~.warehouse.UpdateCollectionRequest):
                    The request object. Request message for
                UpdateCollectionRequest.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Collection:
                    A collection is a resource in a
                corpus. It serves as a container of
                references to original resources.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateCollection._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_collection(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseUpdateCollection._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseUpdateCollection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseUpdateCollection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._UpdateCollection._get_response(
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
            resp = warehouse.Collection()
            pb_resp = warehouse.Collection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_collection(resp)
            return resp

    class _UpdateCorpus(
        _BaseWarehouseRestTransport._BaseUpdateCorpus, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateCorpus")

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
            request: warehouse.UpdateCorpusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.Corpus:
            r"""Call the update corpus method over HTTP.

            Args:
                request (~.warehouse.UpdateCorpusRequest):
                    The request object. Request message for UpdateCorpus.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.Corpus:
                    Corpus is a set of media contents for
                management. Within a corpus, media
                shares the same data schema. Search is
                also restricted within a single corpus.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateCorpus._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_corpus(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseUpdateCorpus._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseUpdateCorpus._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseUpdateCorpus._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._UpdateCorpus._get_response(
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
            resp = warehouse.Corpus()
            pb_resp = warehouse.Corpus.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_corpus(resp)
            return resp

    class _UpdateDataSchema(
        _BaseWarehouseRestTransport._BaseUpdateDataSchema, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateDataSchema")

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
            request: warehouse.UpdateDataSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.DataSchema:
            r"""Call the update data schema method over HTTP.

            Args:
                request (~.warehouse.UpdateDataSchemaRequest):
                    The request object. Request message for UpdateDataSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.DataSchema:
                    Data schema indicates how the user
                specified annotation is interpreted in
                the system.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateDataSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_data_schema(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseUpdateDataSchema._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseUpdateDataSchema._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseUpdateDataSchema._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._UpdateDataSchema._get_response(
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
            resp = warehouse.DataSchema()
            pb_resp = warehouse.DataSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_data_schema(resp)
            return resp

    class _UpdateIndex(_BaseWarehouseRestTransport._BaseUpdateIndex, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateIndex")

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
            request: warehouse.UpdateIndexRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update index method over HTTP.

            Args:
                request (~.warehouse.UpdateIndexRequest):
                    The request object. Request message for UpdateIndex.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateIndex._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_index(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseUpdateIndex._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseUpdateIndex._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseUpdateIndex._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._UpdateIndex._get_response(
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
            resp = self._interceptor.post_update_index(resp)
            return resp

    class _UpdateIndexEndpoint(
        _BaseWarehouseRestTransport._BaseUpdateIndexEndpoint, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateIndexEndpoint")

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
            request: warehouse.UpdateIndexEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update index endpoint method over HTTP.

            Args:
                request (~.warehouse.UpdateIndexEndpointRequest):
                    The request object. Request message for
                UpdateIndexEndpoint.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateIndexEndpoint._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_index_endpoint(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseUpdateIndexEndpoint._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseUpdateIndexEndpoint._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseUpdateIndexEndpoint._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._UpdateIndexEndpoint._get_response(
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
            resp = self._interceptor.post_update_index_endpoint(resp)
            return resp

    class _UpdateSearchConfig(
        _BaseWarehouseRestTransport._BaseUpdateSearchConfig, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateSearchConfig")

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
            request: warehouse.UpdateSearchConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchConfig:
            r"""Call the update search config method over HTTP.

            Args:
                request (~.warehouse.UpdateSearchConfigRequest):
                    The request object. Request message for
                UpdateSearchConfig.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchConfig:
                    SearchConfig stores different
                properties that will affect search
                behaviors and search results.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateSearchConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_search_config(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseUpdateSearchConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseUpdateSearchConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseUpdateSearchConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._UpdateSearchConfig._get_response(
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
            resp = warehouse.SearchConfig()
            pb_resp = warehouse.SearchConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_search_config(resp)
            return resp

    class _UpdateSearchHypernym(
        _BaseWarehouseRestTransport._BaseUpdateSearchHypernym, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.UpdateSearchHypernym")

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
            request: warehouse.UpdateSearchHypernymRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.SearchHypernym:
            r"""Call the update search hypernym method over HTTP.

            Args:
                request (~.warehouse.UpdateSearchHypernymRequest):
                    The request object. Request message for updating
                SearchHypernym.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.SearchHypernym:
                    Search resource: SearchHypernym. For example, {
                hypernym: "vehicle" hyponyms: ["sedan", "truck"] } This
                means in SMART_SEARCH mode, searching for "vehicle" will
                also return results with "sedan" or "truck" as
                annotations.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseUpdateSearchHypernym._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_search_hypernym(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseUpdateSearchHypernym._get_transcoded_request(
                http_options, request
            )

            body = _BaseWarehouseRestTransport._BaseUpdateSearchHypernym._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseUpdateSearchHypernym._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._UpdateSearchHypernym._get_response(
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
            resp = warehouse.SearchHypernym()
            pb_resp = warehouse.SearchHypernym.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_search_hypernym(resp)
            return resp

    class _UploadAsset(_BaseWarehouseRestTransport._BaseUploadAsset, WarehouseRestStub):
        def __hash__(self):
            return hash("WarehouseRestTransport.UploadAsset")

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
            request: warehouse.UploadAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the upload asset method over HTTP.

            Args:
                request (~.warehouse.UploadAssetRequest):
                    The request object. Request message for UploadAsset.
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

            http_options = (
                _BaseWarehouseRestTransport._BaseUploadAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_upload_asset(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseUploadAsset._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWarehouseRestTransport._BaseUploadAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseUploadAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._UploadAsset._get_response(
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
            resp = self._interceptor.post_upload_asset(resp)
            return resp

    class _ViewCollectionItems(
        _BaseWarehouseRestTransport._BaseViewCollectionItems, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ViewCollectionItems")

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
            request: warehouse.ViewCollectionItemsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ViewCollectionItemsResponse:
            r"""Call the view collection items method over HTTP.

            Args:
                request (~.warehouse.ViewCollectionItemsRequest):
                    The request object. Request message for
                ViewCollectionItems.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ViewCollectionItemsResponse:
                    Response message for
                ViewCollectionItems.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseViewCollectionItems._get_http_options()
            )
            request, metadata = self._interceptor.pre_view_collection_items(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseViewCollectionItems._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseViewCollectionItems._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._ViewCollectionItems._get_response(
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
            resp = warehouse.ViewCollectionItemsResponse()
            pb_resp = warehouse.ViewCollectionItemsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_view_collection_items(resp)
            return resp

    class _ViewIndexedAssets(
        _BaseWarehouseRestTransport._BaseViewIndexedAssets, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ViewIndexedAssets")

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
            request: warehouse.ViewIndexedAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> warehouse.ViewIndexedAssetsResponse:
            r"""Call the view indexed assets method over HTTP.

            Args:
                request (~.warehouse.ViewIndexedAssetsRequest):
                    The request object. Request message for
                ViewIndexedAssets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.warehouse.ViewIndexedAssetsResponse:
                    Response message for
                ViewIndexedAssets.

            """

            http_options = (
                _BaseWarehouseRestTransport._BaseViewIndexedAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_view_indexed_assets(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseViewIndexedAssets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseWarehouseRestTransport._BaseViewIndexedAssets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = WarehouseRestTransport._ViewIndexedAssets._get_response(
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
            resp = warehouse.ViewIndexedAssetsResponse()
            pb_resp = warehouse.ViewIndexedAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_view_indexed_assets(resp)
            return resp

    @property
    def add_collection_item(
        self,
    ) -> Callable[
        [warehouse.AddCollectionItemRequest], warehouse.AddCollectionItemResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddCollectionItem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def analyze_asset(
        self,
    ) -> Callable[[warehouse.AnalyzeAssetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnalyzeAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def analyze_corpus(
        self,
    ) -> Callable[[warehouse.AnalyzeCorpusRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AnalyzeCorpus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def clip_asset(
        self,
    ) -> Callable[[warehouse.ClipAssetRequest], warehouse.ClipAssetResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ClipAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_annotation(
        self,
    ) -> Callable[[warehouse.CreateAnnotationRequest], warehouse.Annotation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAnnotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_asset(self) -> Callable[[warehouse.CreateAssetRequest], warehouse.Asset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_collection(
        self,
    ) -> Callable[[warehouse.CreateCollectionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCollection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_corpus(
        self,
    ) -> Callable[[warehouse.CreateCorpusRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCorpus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_data_schema(
        self,
    ) -> Callable[[warehouse.CreateDataSchemaRequest], warehouse.DataSchema]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_index(
        self,
    ) -> Callable[[warehouse.CreateIndexRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateIndex(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_index_endpoint(
        self,
    ) -> Callable[[warehouse.CreateIndexEndpointRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateIndexEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_search_config(
        self,
    ) -> Callable[[warehouse.CreateSearchConfigRequest], warehouse.SearchConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSearchConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_search_hypernym(
        self,
    ) -> Callable[[warehouse.CreateSearchHypernymRequest], warehouse.SearchHypernym]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSearchHypernym(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_annotation(
        self,
    ) -> Callable[[warehouse.DeleteAnnotationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAnnotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_asset(
        self,
    ) -> Callable[[warehouse.DeleteAssetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_collection(
        self,
    ) -> Callable[[warehouse.DeleteCollectionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCollection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_corpus(
        self,
    ) -> Callable[[warehouse.DeleteCorpusRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCorpus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_data_schema(
        self,
    ) -> Callable[[warehouse.DeleteDataSchemaRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_index(
        self,
    ) -> Callable[[warehouse.DeleteIndexRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteIndex(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_index_endpoint(
        self,
    ) -> Callable[[warehouse.DeleteIndexEndpointRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteIndexEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_search_config(
        self,
    ) -> Callable[[warehouse.DeleteSearchConfigRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSearchConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_search_hypernym(
        self,
    ) -> Callable[[warehouse.DeleteSearchHypernymRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSearchHypernym(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def deploy_index(
        self,
    ) -> Callable[[warehouse.DeployIndexRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeployIndex(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_hls_uri(
        self,
    ) -> Callable[[warehouse.GenerateHlsUriRequest], warehouse.GenerateHlsUriResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateHlsUri(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_retrieval_url(
        self,
    ) -> Callable[
        [warehouse.GenerateRetrievalUrlRequest], warehouse.GenerateRetrievalUrlResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateRetrievalUrl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_annotation(
        self,
    ) -> Callable[[warehouse.GetAnnotationRequest], warehouse.Annotation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAnnotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_asset(self) -> Callable[[warehouse.GetAssetRequest], warehouse.Asset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_collection(
        self,
    ) -> Callable[[warehouse.GetCollectionRequest], warehouse.Collection]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCollection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_corpus(self) -> Callable[[warehouse.GetCorpusRequest], warehouse.Corpus]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCorpus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_schema(
        self,
    ) -> Callable[[warehouse.GetDataSchemaRequest], warehouse.DataSchema]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_index(self) -> Callable[[warehouse.GetIndexRequest], warehouse.Index]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIndex(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_index_endpoint(
        self,
    ) -> Callable[[warehouse.GetIndexEndpointRequest], warehouse.IndexEndpoint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIndexEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_search_config(
        self,
    ) -> Callable[[warehouse.GetSearchConfigRequest], warehouse.SearchConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSearchConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_search_hypernym(
        self,
    ) -> Callable[[warehouse.GetSearchHypernymRequest], warehouse.SearchHypernym]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSearchHypernym(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_assets(
        self,
    ) -> Callable[[warehouse.ImportAssetsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def index_asset(
        self,
    ) -> Callable[[warehouse.IndexAssetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._IndexAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def ingest_asset(
        self,
    ) -> Callable[[warehouse.IngestAssetRequest], warehouse.IngestAssetResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._IngestAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_annotations(
        self,
    ) -> Callable[
        [warehouse.ListAnnotationsRequest], warehouse.ListAnnotationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAnnotations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_assets(
        self,
    ) -> Callable[[warehouse.ListAssetsRequest], warehouse.ListAssetsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_collections(
        self,
    ) -> Callable[
        [warehouse.ListCollectionsRequest], warehouse.ListCollectionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCollections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_corpora(
        self,
    ) -> Callable[[warehouse.ListCorporaRequest], warehouse.ListCorporaResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCorpora(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_data_schemas(
        self,
    ) -> Callable[
        [warehouse.ListDataSchemasRequest], warehouse.ListDataSchemasResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDataSchemas(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_index_endpoints(
        self,
    ) -> Callable[
        [warehouse.ListIndexEndpointsRequest], warehouse.ListIndexEndpointsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListIndexEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_indexes(
        self,
    ) -> Callable[[warehouse.ListIndexesRequest], warehouse.ListIndexesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListIndexes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_search_configs(
        self,
    ) -> Callable[
        [warehouse.ListSearchConfigsRequest], warehouse.ListSearchConfigsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSearchConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_search_hypernyms(
        self,
    ) -> Callable[
        [warehouse.ListSearchHypernymsRequest], warehouse.ListSearchHypernymsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSearchHypernyms(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_collection_item(
        self,
    ) -> Callable[
        [warehouse.RemoveCollectionItemRequest], warehouse.RemoveCollectionItemResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveCollectionItem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_index_asset(
        self,
    ) -> Callable[[warehouse.RemoveIndexAssetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveIndexAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_assets(
        self,
    ) -> Callable[[warehouse.SearchAssetsRequest], warehouse.SearchAssetsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_index_endpoint(
        self,
    ) -> Callable[
        [warehouse.SearchIndexEndpointRequest], warehouse.SearchIndexEndpointResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchIndexEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undeploy_index(
        self,
    ) -> Callable[[warehouse.UndeployIndexRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeployIndex(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_annotation(
        self,
    ) -> Callable[[warehouse.UpdateAnnotationRequest], warehouse.Annotation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAnnotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_asset(self) -> Callable[[warehouse.UpdateAssetRequest], warehouse.Asset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_collection(
        self,
    ) -> Callable[[warehouse.UpdateCollectionRequest], warehouse.Collection]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCollection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_corpus(
        self,
    ) -> Callable[[warehouse.UpdateCorpusRequest], warehouse.Corpus]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCorpus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_data_schema(
        self,
    ) -> Callable[[warehouse.UpdateDataSchemaRequest], warehouse.DataSchema]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_index(
        self,
    ) -> Callable[[warehouse.UpdateIndexRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateIndex(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_index_endpoint(
        self,
    ) -> Callable[[warehouse.UpdateIndexEndpointRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateIndexEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_search_config(
        self,
    ) -> Callable[[warehouse.UpdateSearchConfigRequest], warehouse.SearchConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSearchConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_search_hypernym(
        self,
    ) -> Callable[[warehouse.UpdateSearchHypernymRequest], warehouse.SearchHypernym]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSearchHypernym(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def upload_asset(
        self,
    ) -> Callable[[warehouse.UploadAssetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UploadAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def view_collection_items(
        self,
    ) -> Callable[
        [warehouse.ViewCollectionItemsRequest], warehouse.ViewCollectionItemsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ViewCollectionItems(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def view_indexed_assets(
        self,
    ) -> Callable[
        [warehouse.ViewIndexedAssetsRequest], warehouse.ViewIndexedAssetsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ViewIndexedAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseWarehouseRestTransport._BaseCancelOperation, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.CancelOperation")

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

            http_options = (
                _BaseWarehouseRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseWarehouseRestTransport._BaseCancelOperation._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._CancelOperation._get_response(
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
        _BaseWarehouseRestTransport._BaseDeleteOperation, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.DeleteOperation")

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

            http_options = (
                _BaseWarehouseRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseWarehouseRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseDeleteOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._DeleteOperation._get_response(
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
        _BaseWarehouseRestTransport._BaseGetOperation, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.GetOperation")

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

            http_options = (
                _BaseWarehouseRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._GetOperation._get_response(
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
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseWarehouseRestTransport._BaseListOperations, WarehouseRestStub
    ):
        def __hash__(self):
            return hash("WarehouseRestTransport.ListOperations")

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

            http_options = (
                _BaseWarehouseRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseWarehouseRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWarehouseRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WarehouseRestTransport._ListOperations._get_response(
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
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("WarehouseRestTransport",)
