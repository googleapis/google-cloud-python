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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.contact_center_insights_v1.types import (
    contact_center_insights,
    resources,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseContactCenterInsightsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ContactCenterInsightsRestInterceptor:
    """Interceptor for ContactCenterInsights.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ContactCenterInsightsRestTransport.

    .. code-block:: python
        class MyCustomContactCenterInsightsInterceptor(ContactCenterInsightsRestInterceptor):
            def pre_bulk_analyze_conversations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_bulk_analyze_conversations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_bulk_delete_conversations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_bulk_delete_conversations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_calculate_issue_model_stats(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_calculate_issue_model_stats(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_calculate_stats(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_calculate_stats(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_analysis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_analysis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_conversation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_phrase_matcher(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_phrase_matcher(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_view(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_analysis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_issue(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_phrase_matcher(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_deploy_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_deploy_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_insights_data(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_insights_data(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_analysis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_analysis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_conversation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_encryption_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_encryption_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_issue(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_issue(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_phrase_matcher(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_phrase_matcher(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_view(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_ingest_conversations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_ingest_conversations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_initialize_encryption_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_initialize_encryption_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_analyses(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_analyses(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_conversations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_conversations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_issue_models(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_issue_models(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_issues(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_issues(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_phrase_matchers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_phrase_matchers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_views(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_views(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undeploy_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undeploy_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_conversation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_issue(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_issue(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_issue_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_issue_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_phrase_matcher(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_phrase_matcher(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_view(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_upload_conversation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_upload_conversation(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ContactCenterInsightsRestTransport(interceptor=MyCustomContactCenterInsightsInterceptor())
        client = ContactCenterInsightsClient(transport=transport)


    """

    def pre_bulk_analyze_conversations(
        self,
        request: contact_center_insights.BulkAnalyzeConversationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.BulkAnalyzeConversationsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for bulk_analyze_conversations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_bulk_analyze_conversations(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for bulk_analyze_conversations

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_bulk_delete_conversations(
        self,
        request: contact_center_insights.BulkDeleteConversationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.BulkDeleteConversationsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for bulk_delete_conversations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_bulk_delete_conversations(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for bulk_delete_conversations

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_calculate_issue_model_stats(
        self,
        request: contact_center_insights.CalculateIssueModelStatsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.CalculateIssueModelStatsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for calculate_issue_model_stats

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_calculate_issue_model_stats(
        self, response: contact_center_insights.CalculateIssueModelStatsResponse
    ) -> contact_center_insights.CalculateIssueModelStatsResponse:
        """Post-rpc interceptor for calculate_issue_model_stats

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_calculate_stats(
        self,
        request: contact_center_insights.CalculateStatsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.CalculateStatsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for calculate_stats

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_calculate_stats(
        self, response: contact_center_insights.CalculateStatsResponse
    ) -> contact_center_insights.CalculateStatsResponse:
        """Post-rpc interceptor for calculate_stats

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_create_analysis(
        self,
        request: contact_center_insights.CreateAnalysisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.CreateAnalysisRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_analysis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_create_analysis(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_analysis

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_create_conversation(
        self,
        request: contact_center_insights.CreateConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.CreateConversationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_create_conversation(
        self, response: resources.Conversation
    ) -> resources.Conversation:
        """Post-rpc interceptor for create_conversation

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_create_issue_model(
        self,
        request: contact_center_insights.CreateIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.CreateIssueModelRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_create_issue_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_create_phrase_matcher(
        self,
        request: contact_center_insights.CreatePhraseMatcherRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.CreatePhraseMatcherRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_phrase_matcher

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_create_phrase_matcher(
        self, response: resources.PhraseMatcher
    ) -> resources.PhraseMatcher:
        """Post-rpc interceptor for create_phrase_matcher

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_create_view(
        self,
        request: contact_center_insights.CreateViewRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.CreateViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_create_view(self, response: resources.View) -> resources.View:
        """Post-rpc interceptor for create_view

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_delete_analysis(
        self,
        request: contact_center_insights.DeleteAnalysisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.DeleteAnalysisRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_analysis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def pre_delete_conversation(
        self,
        request: contact_center_insights.DeleteConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.DeleteConversationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def pre_delete_issue(
        self,
        request: contact_center_insights.DeleteIssueRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.DeleteIssueRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_issue

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def pre_delete_issue_model(
        self,
        request: contact_center_insights.DeleteIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.DeleteIssueModelRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_delete_issue_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_delete_phrase_matcher(
        self,
        request: contact_center_insights.DeletePhraseMatcherRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.DeletePhraseMatcherRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_phrase_matcher

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def pre_delete_view(
        self,
        request: contact_center_insights.DeleteViewRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.DeleteViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def pre_deploy_issue_model(
        self,
        request: contact_center_insights.DeployIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.DeployIssueModelRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for deploy_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_deploy_issue_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for deploy_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_export_insights_data(
        self,
        request: contact_center_insights.ExportInsightsDataRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.ExportInsightsDataRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for export_insights_data

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_export_insights_data(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_insights_data

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_export_issue_model(
        self,
        request: contact_center_insights.ExportIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.ExportIssueModelRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for export_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_export_issue_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_analysis(
        self,
        request: contact_center_insights.GetAnalysisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.GetAnalysisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_analysis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_analysis(self, response: resources.Analysis) -> resources.Analysis:
        """Post-rpc interceptor for get_analysis

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_conversation(
        self,
        request: contact_center_insights.GetConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.GetConversationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_conversation(
        self, response: resources.Conversation
    ) -> resources.Conversation:
        """Post-rpc interceptor for get_conversation

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_encryption_spec(
        self,
        request: contact_center_insights.GetEncryptionSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.GetEncryptionSpecRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_encryption_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_encryption_spec(
        self, response: resources.EncryptionSpec
    ) -> resources.EncryptionSpec:
        """Post-rpc interceptor for get_encryption_spec

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_issue(
        self,
        request: contact_center_insights.GetIssueRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.GetIssueRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_issue

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_issue(self, response: resources.Issue) -> resources.Issue:
        """Post-rpc interceptor for get_issue

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_issue_model(
        self,
        request: contact_center_insights.GetIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.GetIssueModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_issue_model(
        self, response: resources.IssueModel
    ) -> resources.IssueModel:
        """Post-rpc interceptor for get_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_phrase_matcher(
        self,
        request: contact_center_insights.GetPhraseMatcherRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.GetPhraseMatcherRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_phrase_matcher

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_phrase_matcher(
        self, response: resources.PhraseMatcher
    ) -> resources.PhraseMatcher:
        """Post-rpc interceptor for get_phrase_matcher

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_settings(
        self,
        request: contact_center_insights.GetSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.GetSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_settings(self, response: resources.Settings) -> resources.Settings:
        """Post-rpc interceptor for get_settings

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_get_view(
        self,
        request: contact_center_insights.GetViewRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.GetViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_view(self, response: resources.View) -> resources.View:
        """Post-rpc interceptor for get_view

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_import_issue_model(
        self,
        request: contact_center_insights.ImportIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.ImportIssueModelRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for import_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_import_issue_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_ingest_conversations(
        self,
        request: contact_center_insights.IngestConversationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.IngestConversationsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for ingest_conversations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_ingest_conversations(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for ingest_conversations

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_initialize_encryption_spec(
        self,
        request: contact_center_insights.InitializeEncryptionSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.InitializeEncryptionSpecRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for initialize_encryption_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_initialize_encryption_spec(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for initialize_encryption_spec

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_analyses(
        self,
        request: contact_center_insights.ListAnalysesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.ListAnalysesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_analyses

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_list_analyses(
        self, response: contact_center_insights.ListAnalysesResponse
    ) -> contact_center_insights.ListAnalysesResponse:
        """Post-rpc interceptor for list_analyses

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_conversations(
        self,
        request: contact_center_insights.ListConversationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.ListConversationsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_conversations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_list_conversations(
        self, response: contact_center_insights.ListConversationsResponse
    ) -> contact_center_insights.ListConversationsResponse:
        """Post-rpc interceptor for list_conversations

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_issue_models(
        self,
        request: contact_center_insights.ListIssueModelsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.ListIssueModelsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_issue_models

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_list_issue_models(
        self, response: contact_center_insights.ListIssueModelsResponse
    ) -> contact_center_insights.ListIssueModelsResponse:
        """Post-rpc interceptor for list_issue_models

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_issues(
        self,
        request: contact_center_insights.ListIssuesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.ListIssuesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_issues

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_list_issues(
        self, response: contact_center_insights.ListIssuesResponse
    ) -> contact_center_insights.ListIssuesResponse:
        """Post-rpc interceptor for list_issues

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_phrase_matchers(
        self,
        request: contact_center_insights.ListPhraseMatchersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.ListPhraseMatchersRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_phrase_matchers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_list_phrase_matchers(
        self, response: contact_center_insights.ListPhraseMatchersResponse
    ) -> contact_center_insights.ListPhraseMatchersResponse:
        """Post-rpc interceptor for list_phrase_matchers

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_list_views(
        self,
        request: contact_center_insights.ListViewsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.ListViewsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_views

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_list_views(
        self, response: contact_center_insights.ListViewsResponse
    ) -> contact_center_insights.ListViewsResponse:
        """Post-rpc interceptor for list_views

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_undeploy_issue_model(
        self,
        request: contact_center_insights.UndeployIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.UndeployIssueModelRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for undeploy_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_undeploy_issue_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undeploy_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_update_conversation(
        self,
        request: contact_center_insights.UpdateConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.UpdateConversationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_update_conversation(
        self, response: resources.Conversation
    ) -> resources.Conversation:
        """Post-rpc interceptor for update_conversation

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_update_issue(
        self,
        request: contact_center_insights.UpdateIssueRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.UpdateIssueRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_issue

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_update_issue(self, response: resources.Issue) -> resources.Issue:
        """Post-rpc interceptor for update_issue

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_update_issue_model(
        self,
        request: contact_center_insights.UpdateIssueModelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.UpdateIssueModelRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_issue_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_update_issue_model(
        self, response: resources.IssueModel
    ) -> resources.IssueModel:
        """Post-rpc interceptor for update_issue_model

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_update_phrase_matcher(
        self,
        request: contact_center_insights.UpdatePhraseMatcherRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.UpdatePhraseMatcherRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_phrase_matcher

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_update_phrase_matcher(
        self, response: resources.PhraseMatcher
    ) -> resources.PhraseMatcher:
        """Post-rpc interceptor for update_phrase_matcher

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_update_settings(
        self,
        request: contact_center_insights.UpdateSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.UpdateSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_update_settings(self, response: resources.Settings) -> resources.Settings:
        """Post-rpc interceptor for update_settings

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_update_view(
        self,
        request: contact_center_insights.UpdateViewRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[contact_center_insights.UpdateViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_update_view(self, response: resources.View) -> resources.View:
        """Post-rpc interceptor for update_view

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response

    def pre_upload_conversation(
        self,
        request: contact_center_insights.UploadConversationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        contact_center_insights.UploadConversationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for upload_conversation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_upload_conversation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for upload_conversation

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
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
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
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
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
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
        before they are sent to the ContactCenterInsights server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ContactCenterInsights server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ContactCenterInsightsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ContactCenterInsightsRestInterceptor


class ContactCenterInsightsRestTransport(_BaseContactCenterInsightsRestTransport):
    """REST backend synchronous transport for ContactCenterInsights.

    An API that lets users analyze and explore their business
    conversation data.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "contactcenterinsights.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ContactCenterInsightsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'contactcenterinsights.googleapis.com').
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
        self._interceptor = interceptor or ContactCenterInsightsRestInterceptor()
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
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
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

    class _BulkAnalyzeConversations(
        _BaseContactCenterInsightsRestTransport._BaseBulkAnalyzeConversations,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.BulkAnalyzeConversations")

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
            request: contact_center_insights.BulkAnalyzeConversationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the bulk analyze
            conversations method over HTTP.

                Args:
                    request (~.contact_center_insights.BulkAnalyzeConversationsRequest):
                        The request object. The request to analyze conversations
                    in bulk.
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
                _BaseContactCenterInsightsRestTransport._BaseBulkAnalyzeConversations._get_http_options()
            )
            request, metadata = self._interceptor.pre_bulk_analyze_conversations(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseBulkAnalyzeConversations._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseBulkAnalyzeConversations._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseBulkAnalyzeConversations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._BulkAnalyzeConversations._get_response(
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
            resp = self._interceptor.post_bulk_analyze_conversations(resp)
            return resp

    class _BulkDeleteConversations(
        _BaseContactCenterInsightsRestTransport._BaseBulkDeleteConversations,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.BulkDeleteConversations")

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
            request: contact_center_insights.BulkDeleteConversationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the bulk delete conversations method over HTTP.

            Args:
                request (~.contact_center_insights.BulkDeleteConversationsRequest):
                    The request object. The request to delete conversations
                in bulk.
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
                _BaseContactCenterInsightsRestTransport._BaseBulkDeleteConversations._get_http_options()
            )
            request, metadata = self._interceptor.pre_bulk_delete_conversations(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseBulkDeleteConversations._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseBulkDeleteConversations._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseBulkDeleteConversations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._BulkDeleteConversations._get_response(
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
            resp = self._interceptor.post_bulk_delete_conversations(resp)
            return resp

    class _CalculateIssueModelStats(
        _BaseContactCenterInsightsRestTransport._BaseCalculateIssueModelStats,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CalculateIssueModelStats")

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
            request: contact_center_insights.CalculateIssueModelStatsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.CalculateIssueModelStatsResponse:
            r"""Call the calculate issue model
            stats method over HTTP.

                Args:
                    request (~.contact_center_insights.CalculateIssueModelStatsRequest):
                        The request object. Request to get statistics of an issue
                    model.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.contact_center_insights.CalculateIssueModelStatsResponse:
                        Response of querying an issue model's
                    statistics.

            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseCalculateIssueModelStats._get_http_options()
            )
            request, metadata = self._interceptor.pre_calculate_issue_model_stats(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCalculateIssueModelStats._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCalculateIssueModelStats._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._CalculateIssueModelStats._get_response(
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
            resp = contact_center_insights.CalculateIssueModelStatsResponse()
            pb_resp = contact_center_insights.CalculateIssueModelStatsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_calculate_issue_model_stats(resp)
            return resp

    class _CalculateStats(
        _BaseContactCenterInsightsRestTransport._BaseCalculateStats,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CalculateStats")

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
            request: contact_center_insights.CalculateStatsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.CalculateStatsResponse:
            r"""Call the calculate stats method over HTTP.

            Args:
                request (~.contact_center_insights.CalculateStatsRequest):
                    The request object. The request for calculating
                conversation statistics.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.contact_center_insights.CalculateStatsResponse:
                    The response for calculating
                conversation statistics.

            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseCalculateStats._get_http_options()
            )
            request, metadata = self._interceptor.pre_calculate_stats(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCalculateStats._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCalculateStats._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._CalculateStats._get_response(
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
            resp = contact_center_insights.CalculateStatsResponse()
            pb_resp = contact_center_insights.CalculateStatsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_calculate_stats(resp)
            return resp

    class _CreateAnalysis(
        _BaseContactCenterInsightsRestTransport._BaseCreateAnalysis,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CreateAnalysis")

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
            request: contact_center_insights.CreateAnalysisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create analysis method over HTTP.

            Args:
                request (~.contact_center_insights.CreateAnalysisRequest):
                    The request object. The request to create an analysis.
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
                _BaseContactCenterInsightsRestTransport._BaseCreateAnalysis._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_analysis(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCreateAnalysis._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseCreateAnalysis._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCreateAnalysis._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._CreateAnalysis._get_response(
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
            resp = self._interceptor.post_create_analysis(resp)
            return resp

    class _CreateConversation(
        _BaseContactCenterInsightsRestTransport._BaseCreateConversation,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CreateConversation")

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
            request: contact_center_insights.CreateConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Conversation:
            r"""Call the create conversation method over HTTP.

            Args:
                request (~.contact_center_insights.CreateConversationRequest):
                    The request object. Request to create a conversation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Conversation:
                    The conversation resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseCreateConversation._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_conversation(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCreateConversation._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseCreateConversation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCreateConversation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._CreateConversation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Conversation()
            pb_resp = resources.Conversation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_conversation(resp)
            return resp

    class _CreateIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseCreateIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CreateIssueModel")

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
            request: contact_center_insights.CreateIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create issue model method over HTTP.

            Args:
                request (~.contact_center_insights.CreateIssueModelRequest):
                    The request object. The request to create an issue model.
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
                _BaseContactCenterInsightsRestTransport._BaseCreateIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_issue_model(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCreateIssueModel._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseCreateIssueModel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCreateIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._CreateIssueModel._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_issue_model(resp)
            return resp

    class _CreatePhraseMatcher(
        _BaseContactCenterInsightsRestTransport._BaseCreatePhraseMatcher,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CreatePhraseMatcher")

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
            request: contact_center_insights.CreatePhraseMatcherRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.PhraseMatcher:
            r"""Call the create phrase matcher method over HTTP.

            Args:
                request (~.contact_center_insights.CreatePhraseMatcherRequest):
                    The request object. Request to create a phrase matcher.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.PhraseMatcher:
                    The phrase matcher resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseCreatePhraseMatcher._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_phrase_matcher(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCreatePhraseMatcher._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseCreatePhraseMatcher._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCreatePhraseMatcher._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._CreatePhraseMatcher._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.PhraseMatcher()
            pb_resp = resources.PhraseMatcher.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_phrase_matcher(resp)
            return resp

    class _CreateView(
        _BaseContactCenterInsightsRestTransport._BaseCreateView,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CreateView")

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
            request: contact_center_insights.CreateViewRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.View:
            r"""Call the create view method over HTTP.

            Args:
                request (~.contact_center_insights.CreateViewRequest):
                    The request object. The request to create a view.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.View:
                    The View resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseCreateView._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_view(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCreateView._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseCreateView._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCreateView._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._CreateView._get_response(
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
            resp = resources.View()
            pb_resp = resources.View.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_view(resp)
            return resp

    class _DeleteAnalysis(
        _BaseContactCenterInsightsRestTransport._BaseDeleteAnalysis,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.DeleteAnalysis")

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
            request: contact_center_insights.DeleteAnalysisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete analysis method over HTTP.

            Args:
                request (~.contact_center_insights.DeleteAnalysisRequest):
                    The request object. The request to delete an analysis.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseDeleteAnalysis._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_analysis(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseDeleteAnalysis._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseDeleteAnalysis._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._DeleteAnalysis._get_response(
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

    class _DeleteConversation(
        _BaseContactCenterInsightsRestTransport._BaseDeleteConversation,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.DeleteConversation")

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
            request: contact_center_insights.DeleteConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete conversation method over HTTP.

            Args:
                request (~.contact_center_insights.DeleteConversationRequest):
                    The request object. The request to delete a conversation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseDeleteConversation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_conversation(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseDeleteConversation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseDeleteConversation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._DeleteConversation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteIssue(
        _BaseContactCenterInsightsRestTransport._BaseDeleteIssue,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.DeleteIssue")

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
            request: contact_center_insights.DeleteIssueRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete issue method over HTTP.

            Args:
                request (~.contact_center_insights.DeleteIssueRequest):
                    The request object. The request to delete an issue.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseDeleteIssue._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_issue(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseDeleteIssue._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseDeleteIssue._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._DeleteIssue._get_response(
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

    class _DeleteIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseDeleteIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.DeleteIssueModel")

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
            request: contact_center_insights.DeleteIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete issue model method over HTTP.

            Args:
                request (~.contact_center_insights.DeleteIssueModelRequest):
                    The request object. The request to delete an issue model.
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
                _BaseContactCenterInsightsRestTransport._BaseDeleteIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_issue_model(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseDeleteIssueModel._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseDeleteIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._DeleteIssueModel._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_issue_model(resp)
            return resp

    class _DeletePhraseMatcher(
        _BaseContactCenterInsightsRestTransport._BaseDeletePhraseMatcher,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.DeletePhraseMatcher")

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
            request: contact_center_insights.DeletePhraseMatcherRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete phrase matcher method over HTTP.

            Args:
                request (~.contact_center_insights.DeletePhraseMatcherRequest):
                    The request object. The request to delete a phrase
                matcher.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseDeletePhraseMatcher._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_phrase_matcher(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseDeletePhraseMatcher._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseDeletePhraseMatcher._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._DeletePhraseMatcher._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteView(
        _BaseContactCenterInsightsRestTransport._BaseDeleteView,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.DeleteView")

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
            request: contact_center_insights.DeleteViewRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete view method over HTTP.

            Args:
                request (~.contact_center_insights.DeleteViewRequest):
                    The request object. The request to delete a view.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseDeleteView._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_view(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseDeleteView._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseDeleteView._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._DeleteView._get_response(
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

    class _DeployIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseDeployIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.DeployIssueModel")

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
            request: contact_center_insights.DeployIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the deploy issue model method over HTTP.

            Args:
                request (~.contact_center_insights.DeployIssueModelRequest):
                    The request object. The request to deploy an issue model.
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
                _BaseContactCenterInsightsRestTransport._BaseDeployIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_deploy_issue_model(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseDeployIssueModel._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseDeployIssueModel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseDeployIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._DeployIssueModel._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_deploy_issue_model(resp)
            return resp

    class _ExportInsightsData(
        _BaseContactCenterInsightsRestTransport._BaseExportInsightsData,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ExportInsightsData")

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
            request: contact_center_insights.ExportInsightsDataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export insights data method over HTTP.

            Args:
                request (~.contact_center_insights.ExportInsightsDataRequest):
                    The request object. The request to export insights.
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
                _BaseContactCenterInsightsRestTransport._BaseExportInsightsData._get_http_options()
            )
            request, metadata = self._interceptor.pre_export_insights_data(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseExportInsightsData._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseExportInsightsData._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseExportInsightsData._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._ExportInsightsData._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_insights_data(resp)
            return resp

    class _ExportIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseExportIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ExportIssueModel")

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
            request: contact_center_insights.ExportIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export issue model method over HTTP.

            Args:
                request (~.contact_center_insights.ExportIssueModelRequest):
                    The request object. Request to export an issue model.
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
                _BaseContactCenterInsightsRestTransport._BaseExportIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_export_issue_model(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseExportIssueModel._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseExportIssueModel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseExportIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._ExportIssueModel._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_issue_model(resp)
            return resp

    class _GetAnalysis(
        _BaseContactCenterInsightsRestTransport._BaseGetAnalysis,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetAnalysis")

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
            request: contact_center_insights.GetAnalysisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Analysis:
            r"""Call the get analysis method over HTTP.

            Args:
                request (~.contact_center_insights.GetAnalysisRequest):
                    The request object. The request to get an analysis.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Analysis:
                    The analysis resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetAnalysis._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_analysis(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetAnalysis._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetAnalysis._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._GetAnalysis._get_response(
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
            resp = resources.Analysis()
            pb_resp = resources.Analysis.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_analysis(resp)
            return resp

    class _GetConversation(
        _BaseContactCenterInsightsRestTransport._BaseGetConversation,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetConversation")

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
            request: contact_center_insights.GetConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Conversation:
            r"""Call the get conversation method over HTTP.

            Args:
                request (~.contact_center_insights.GetConversationRequest):
                    The request object. The request to get a conversation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Conversation:
                    The conversation resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetConversation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_conversation(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetConversation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetConversation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._GetConversation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Conversation()
            pb_resp = resources.Conversation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_conversation(resp)
            return resp

    class _GetEncryptionSpec(
        _BaseContactCenterInsightsRestTransport._BaseGetEncryptionSpec,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetEncryptionSpec")

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
            request: contact_center_insights.GetEncryptionSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.EncryptionSpec:
            r"""Call the get encryption spec method over HTTP.

            Args:
                request (~.contact_center_insights.GetEncryptionSpecRequest):
                    The request object. The request to get location-level
                encryption specification.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.EncryptionSpec:
                    A customer-managed encryption key
                specification that can be applied to all
                created resources (e.g. Conversation).

            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetEncryptionSpec._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_encryption_spec(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetEncryptionSpec._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetEncryptionSpec._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._GetEncryptionSpec._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.EncryptionSpec()
            pb_resp = resources.EncryptionSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_encryption_spec(resp)
            return resp

    class _GetIssue(
        _BaseContactCenterInsightsRestTransport._BaseGetIssue,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetIssue")

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
            request: contact_center_insights.GetIssueRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Issue:
            r"""Call the get issue method over HTTP.

            Args:
                request (~.contact_center_insights.GetIssueRequest):
                    The request object. The request to get an issue.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Issue:
                    The issue resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetIssue._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_issue(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetIssue._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetIssue._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._GetIssue._get_response(
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
            resp = resources.Issue()
            pb_resp = resources.Issue.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_issue(resp)
            return resp

    class _GetIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseGetIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetIssueModel")

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
            request: contact_center_insights.GetIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.IssueModel:
            r"""Call the get issue model method over HTTP.

            Args:
                request (~.contact_center_insights.GetIssueModelRequest):
                    The request object. The request to get an issue model.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.IssueModel:
                    The issue model resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_issue_model(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetIssueModel._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._GetIssueModel._get_response(
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
            resp = resources.IssueModel()
            pb_resp = resources.IssueModel.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_issue_model(resp)
            return resp

    class _GetPhraseMatcher(
        _BaseContactCenterInsightsRestTransport._BaseGetPhraseMatcher,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetPhraseMatcher")

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
            request: contact_center_insights.GetPhraseMatcherRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.PhraseMatcher:
            r"""Call the get phrase matcher method over HTTP.

            Args:
                request (~.contact_center_insights.GetPhraseMatcherRequest):
                    The request object. The request to get a a phrase
                matcher.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.PhraseMatcher:
                    The phrase matcher resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetPhraseMatcher._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_phrase_matcher(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetPhraseMatcher._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetPhraseMatcher._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._GetPhraseMatcher._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.PhraseMatcher()
            pb_resp = resources.PhraseMatcher.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_phrase_matcher(resp)
            return resp

    class _GetSettings(
        _BaseContactCenterInsightsRestTransport._BaseGetSettings,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetSettings")

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
            request: contact_center_insights.GetSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Settings:
            r"""Call the get settings method over HTTP.

            Args:
                request (~.contact_center_insights.GetSettingsRequest):
                    The request object. The request to get project-level
                settings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Settings:
                    The CCAI Insights project wide settings. Use these
                settings to configure the behavior of Insights. View
                these settings with
                ```getsettings`` <https://cloud.google.com/contact-center/insights/docs/reference/rest/v1/projects.locations/getSettings>`__
                and change the settings with
                ```updateSettings`` <https://cloud.google.com/contact-center/insights/docs/reference/rest/v1/projects.locations/updateSettings>`__.

            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetSettings._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_settings(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetSettings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetSettings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._GetSettings._get_response(
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
            resp = resources.Settings()
            pb_resp = resources.Settings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_settings(resp)
            return resp

    class _GetView(
        _BaseContactCenterInsightsRestTransport._BaseGetView,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetView")

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
            request: contact_center_insights.GetViewRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.View:
            r"""Call the get view method over HTTP.

            Args:
                request (~.contact_center_insights.GetViewRequest):
                    The request object. The request to get a view.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.View:
                    The View resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseGetView._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_view(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetView._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetView._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._GetView._get_response(
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
            resp = resources.View()
            pb_resp = resources.View.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_view(resp)
            return resp

    class _ImportIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseImportIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ImportIssueModel")

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
            request: contact_center_insights.ImportIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import issue model method over HTTP.

            Args:
                request (~.contact_center_insights.ImportIssueModelRequest):
                    The request object. Request to import an issue model.
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
                _BaseContactCenterInsightsRestTransport._BaseImportIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_import_issue_model(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseImportIssueModel._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseImportIssueModel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseImportIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._ImportIssueModel._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_issue_model(resp)
            return resp

    class _IngestConversations(
        _BaseContactCenterInsightsRestTransport._BaseIngestConversations,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.IngestConversations")

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
            request: contact_center_insights.IngestConversationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the ingest conversations method over HTTP.

            Args:
                request (~.contact_center_insights.IngestConversationsRequest):
                    The request object. The request to ingest conversations.
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
                _BaseContactCenterInsightsRestTransport._BaseIngestConversations._get_http_options()
            )
            request, metadata = self._interceptor.pre_ingest_conversations(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseIngestConversations._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseIngestConversations._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseIngestConversations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._IngestConversations._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_ingest_conversations(resp)
            return resp

    class _InitializeEncryptionSpec(
        _BaseContactCenterInsightsRestTransport._BaseInitializeEncryptionSpec,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.InitializeEncryptionSpec")

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
            request: contact_center_insights.InitializeEncryptionSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the initialize encryption
            spec method over HTTP.

                Args:
                    request (~.contact_center_insights.InitializeEncryptionSpecRequest):
                        The request object. The request to initialize a
                    location-level encryption specification.
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
                _BaseContactCenterInsightsRestTransport._BaseInitializeEncryptionSpec._get_http_options()
            )
            request, metadata = self._interceptor.pre_initialize_encryption_spec(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseInitializeEncryptionSpec._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseInitializeEncryptionSpec._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseInitializeEncryptionSpec._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._InitializeEncryptionSpec._get_response(
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
            resp = self._interceptor.post_initialize_encryption_spec(resp)
            return resp

    class _ListAnalyses(
        _BaseContactCenterInsightsRestTransport._BaseListAnalyses,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ListAnalyses")

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
            request: contact_center_insights.ListAnalysesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.ListAnalysesResponse:
            r"""Call the list analyses method over HTTP.

            Args:
                request (~.contact_center_insights.ListAnalysesRequest):
                    The request object. The request to list analyses.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.contact_center_insights.ListAnalysesResponse:
                    The response to list analyses.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseListAnalyses._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_analyses(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseListAnalyses._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseListAnalyses._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._ListAnalyses._get_response(
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
            resp = contact_center_insights.ListAnalysesResponse()
            pb_resp = contact_center_insights.ListAnalysesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_analyses(resp)
            return resp

    class _ListConversations(
        _BaseContactCenterInsightsRestTransport._BaseListConversations,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ListConversations")

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
            request: contact_center_insights.ListConversationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.ListConversationsResponse:
            r"""Call the list conversations method over HTTP.

            Args:
                request (~.contact_center_insights.ListConversationsRequest):
                    The request object. Request to list conversations.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.contact_center_insights.ListConversationsResponse:
                    The response of listing
                conversations.

            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseListConversations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_conversations(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseListConversations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseListConversations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._ListConversations._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = contact_center_insights.ListConversationsResponse()
            pb_resp = contact_center_insights.ListConversationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_conversations(resp)
            return resp

    class _ListIssueModels(
        _BaseContactCenterInsightsRestTransport._BaseListIssueModels,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ListIssueModels")

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
            request: contact_center_insights.ListIssueModelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.ListIssueModelsResponse:
            r"""Call the list issue models method over HTTP.

            Args:
                request (~.contact_center_insights.ListIssueModelsRequest):
                    The request object. Request to list issue models.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.contact_center_insights.ListIssueModelsResponse:
                    The response of listing issue models.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseListIssueModels._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_issue_models(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseListIssueModels._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseListIssueModels._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._ListIssueModels._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = contact_center_insights.ListIssueModelsResponse()
            pb_resp = contact_center_insights.ListIssueModelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_issue_models(resp)
            return resp

    class _ListIssues(
        _BaseContactCenterInsightsRestTransport._BaseListIssues,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ListIssues")

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
            request: contact_center_insights.ListIssuesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.ListIssuesResponse:
            r"""Call the list issues method over HTTP.

            Args:
                request (~.contact_center_insights.ListIssuesRequest):
                    The request object. Request to list issues.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.contact_center_insights.ListIssuesResponse:
                    The response of listing issues.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseListIssues._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_issues(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseListIssues._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseListIssues._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._ListIssues._get_response(
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
            resp = contact_center_insights.ListIssuesResponse()
            pb_resp = contact_center_insights.ListIssuesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_issues(resp)
            return resp

    class _ListPhraseMatchers(
        _BaseContactCenterInsightsRestTransport._BaseListPhraseMatchers,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ListPhraseMatchers")

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
            request: contact_center_insights.ListPhraseMatchersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.ListPhraseMatchersResponse:
            r"""Call the list phrase matchers method over HTTP.

            Args:
                request (~.contact_center_insights.ListPhraseMatchersRequest):
                    The request object. Request to list phrase matchers.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.contact_center_insights.ListPhraseMatchersResponse:
                    The response of listing phrase
                matchers.

            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseListPhraseMatchers._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_phrase_matchers(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseListPhraseMatchers._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseListPhraseMatchers._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._ListPhraseMatchers._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = contact_center_insights.ListPhraseMatchersResponse()
            pb_resp = contact_center_insights.ListPhraseMatchersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_phrase_matchers(resp)
            return resp

    class _ListViews(
        _BaseContactCenterInsightsRestTransport._BaseListViews,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ListViews")

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
            request: contact_center_insights.ListViewsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> contact_center_insights.ListViewsResponse:
            r"""Call the list views method over HTTP.

            Args:
                request (~.contact_center_insights.ListViewsRequest):
                    The request object. The request to list views.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.contact_center_insights.ListViewsResponse:
                    The response of listing views.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseListViews._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_views(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseListViews._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseListViews._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._ListViews._get_response(
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
            resp = contact_center_insights.ListViewsResponse()
            pb_resp = contact_center_insights.ListViewsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_views(resp)
            return resp

    class _UndeployIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseUndeployIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UndeployIssueModel")

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
            request: contact_center_insights.UndeployIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undeploy issue model method over HTTP.

            Args:
                request (~.contact_center_insights.UndeployIssueModelRequest):
                    The request object. The request to undeploy an issue
                model.
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
                _BaseContactCenterInsightsRestTransport._BaseUndeployIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_undeploy_issue_model(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUndeployIssueModel._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUndeployIssueModel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUndeployIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._UndeployIssueModel._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_undeploy_issue_model(resp)
            return resp

    class _UpdateConversation(
        _BaseContactCenterInsightsRestTransport._BaseUpdateConversation,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UpdateConversation")

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
            request: contact_center_insights.UpdateConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Conversation:
            r"""Call the update conversation method over HTTP.

            Args:
                request (~.contact_center_insights.UpdateConversationRequest):
                    The request object. The request to update a conversation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Conversation:
                    The conversation resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseUpdateConversation._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_conversation(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUpdateConversation._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUpdateConversation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUpdateConversation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._UpdateConversation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Conversation()
            pb_resp = resources.Conversation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_conversation(resp)
            return resp

    class _UpdateIssue(
        _BaseContactCenterInsightsRestTransport._BaseUpdateIssue,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UpdateIssue")

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
            request: contact_center_insights.UpdateIssueRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Issue:
            r"""Call the update issue method over HTTP.

            Args:
                request (~.contact_center_insights.UpdateIssueRequest):
                    The request object. The request to update an issue.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Issue:
                    The issue resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseUpdateIssue._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_issue(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUpdateIssue._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUpdateIssue._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUpdateIssue._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._UpdateIssue._get_response(
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
            resp = resources.Issue()
            pb_resp = resources.Issue.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_issue(resp)
            return resp

    class _UpdateIssueModel(
        _BaseContactCenterInsightsRestTransport._BaseUpdateIssueModel,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UpdateIssueModel")

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
            request: contact_center_insights.UpdateIssueModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.IssueModel:
            r"""Call the update issue model method over HTTP.

            Args:
                request (~.contact_center_insights.UpdateIssueModelRequest):
                    The request object. The request to update an issue model.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.IssueModel:
                    The issue model resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseUpdateIssueModel._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_issue_model(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUpdateIssueModel._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUpdateIssueModel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUpdateIssueModel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._UpdateIssueModel._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.IssueModel()
            pb_resp = resources.IssueModel.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_issue_model(resp)
            return resp

    class _UpdatePhraseMatcher(
        _BaseContactCenterInsightsRestTransport._BaseUpdatePhraseMatcher,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UpdatePhraseMatcher")

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
            request: contact_center_insights.UpdatePhraseMatcherRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.PhraseMatcher:
            r"""Call the update phrase matcher method over HTTP.

            Args:
                request (~.contact_center_insights.UpdatePhraseMatcherRequest):
                    The request object. The request to update a phrase
                matcher.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.PhraseMatcher:
                    The phrase matcher resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseUpdatePhraseMatcher._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_phrase_matcher(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUpdatePhraseMatcher._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUpdatePhraseMatcher._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUpdatePhraseMatcher._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._UpdatePhraseMatcher._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.PhraseMatcher()
            pb_resp = resources.PhraseMatcher.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_phrase_matcher(resp)
            return resp

    class _UpdateSettings(
        _BaseContactCenterInsightsRestTransport._BaseUpdateSettings,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UpdateSettings")

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
            request: contact_center_insights.UpdateSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Settings:
            r"""Call the update settings method over HTTP.

            Args:
                request (~.contact_center_insights.UpdateSettingsRequest):
                    The request object. The request to update project-level
                settings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Settings:
                    The CCAI Insights project wide settings. Use these
                settings to configure the behavior of Insights. View
                these settings with
                ```getsettings`` <https://cloud.google.com/contact-center/insights/docs/reference/rest/v1/projects.locations/getSettings>`__
                and change the settings with
                ```updateSettings`` <https://cloud.google.com/contact-center/insights/docs/reference/rest/v1/projects.locations/updateSettings>`__.

            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseUpdateSettings._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_settings(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUpdateSettings._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUpdateSettings._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUpdateSettings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._UpdateSettings._get_response(
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
            resp = resources.Settings()
            pb_resp = resources.Settings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_settings(resp)
            return resp

    class _UpdateView(
        _BaseContactCenterInsightsRestTransport._BaseUpdateView,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UpdateView")

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
            request: contact_center_insights.UpdateViewRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.View:
            r"""Call the update view method over HTTP.

            Args:
                request (~.contact_center_insights.UpdateViewRequest):
                    The request object. The request to update a view.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.View:
                    The View resource.
            """

            http_options = (
                _BaseContactCenterInsightsRestTransport._BaseUpdateView._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_view(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUpdateView._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUpdateView._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUpdateView._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._UpdateView._get_response(
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
            resp = resources.View()
            pb_resp = resources.View.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_view(resp)
            return resp

    class _UploadConversation(
        _BaseContactCenterInsightsRestTransport._BaseUploadConversation,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.UploadConversation")

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
            request: contact_center_insights.UploadConversationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the upload conversation method over HTTP.

            Args:
                request (~.contact_center_insights.UploadConversationRequest):
                    The request object. Request to upload a conversation.
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
                _BaseContactCenterInsightsRestTransport._BaseUploadConversation._get_http_options()
            )
            request, metadata = self._interceptor.pre_upload_conversation(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseUploadConversation._get_transcoded_request(
                http_options, request
            )

            body = _BaseContactCenterInsightsRestTransport._BaseUploadConversation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseUploadConversation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._UploadConversation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_upload_conversation(resp)
            return resp

    @property
    def bulk_analyze_conversations(
        self,
    ) -> Callable[
        [contact_center_insights.BulkAnalyzeConversationsRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BulkAnalyzeConversations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def bulk_delete_conversations(
        self,
    ) -> Callable[
        [contact_center_insights.BulkDeleteConversationsRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BulkDeleteConversations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def calculate_issue_model_stats(
        self,
    ) -> Callable[
        [contact_center_insights.CalculateIssueModelStatsRequest],
        contact_center_insights.CalculateIssueModelStatsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CalculateIssueModelStats(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def calculate_stats(
        self,
    ) -> Callable[
        [contact_center_insights.CalculateStatsRequest],
        contact_center_insights.CalculateStatsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CalculateStats(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_analysis(
        self,
    ) -> Callable[
        [contact_center_insights.CreateAnalysisRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAnalysis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_conversation(
        self,
    ) -> Callable[
        [contact_center_insights.CreateConversationRequest], resources.Conversation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_issue_model(
        self,
    ) -> Callable[
        [contact_center_insights.CreateIssueModelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_phrase_matcher(
        self,
    ) -> Callable[
        [contact_center_insights.CreatePhraseMatcherRequest], resources.PhraseMatcher
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePhraseMatcher(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_view(
        self,
    ) -> Callable[[contact_center_insights.CreateViewRequest], resources.View]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateView(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_analysis(
        self,
    ) -> Callable[[contact_center_insights.DeleteAnalysisRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAnalysis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_conversation(
        self,
    ) -> Callable[[contact_center_insights.DeleteConversationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_issue(
        self,
    ) -> Callable[[contact_center_insights.DeleteIssueRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteIssue(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_issue_model(
        self,
    ) -> Callable[
        [contact_center_insights.DeleteIssueModelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_phrase_matcher(
        self,
    ) -> Callable[
        [contact_center_insights.DeletePhraseMatcherRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePhraseMatcher(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_view(
        self,
    ) -> Callable[[contact_center_insights.DeleteViewRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteView(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def deploy_issue_model(
        self,
    ) -> Callable[
        [contact_center_insights.DeployIssueModelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeployIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_insights_data(
        self,
    ) -> Callable[
        [contact_center_insights.ExportInsightsDataRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportInsightsData(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_issue_model(
        self,
    ) -> Callable[
        [contact_center_insights.ExportIssueModelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_analysis(
        self,
    ) -> Callable[[contact_center_insights.GetAnalysisRequest], resources.Analysis]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAnalysis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_conversation(
        self,
    ) -> Callable[
        [contact_center_insights.GetConversationRequest], resources.Conversation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_encryption_spec(
        self,
    ) -> Callable[
        [contact_center_insights.GetEncryptionSpecRequest], resources.EncryptionSpec
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEncryptionSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_issue(
        self,
    ) -> Callable[[contact_center_insights.GetIssueRequest], resources.Issue]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIssue(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_issue_model(
        self,
    ) -> Callable[[contact_center_insights.GetIssueModelRequest], resources.IssueModel]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_phrase_matcher(
        self,
    ) -> Callable[
        [contact_center_insights.GetPhraseMatcherRequest], resources.PhraseMatcher
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPhraseMatcher(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_settings(
        self,
    ) -> Callable[[contact_center_insights.GetSettingsRequest], resources.Settings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_view(
        self,
    ) -> Callable[[contact_center_insights.GetViewRequest], resources.View]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetView(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_issue_model(
        self,
    ) -> Callable[
        [contact_center_insights.ImportIssueModelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def ingest_conversations(
        self,
    ) -> Callable[
        [contact_center_insights.IngestConversationsRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._IngestConversations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def initialize_encryption_spec(
        self,
    ) -> Callable[
        [contact_center_insights.InitializeEncryptionSpecRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InitializeEncryptionSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_analyses(
        self,
    ) -> Callable[
        [contact_center_insights.ListAnalysesRequest],
        contact_center_insights.ListAnalysesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAnalyses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_conversations(
        self,
    ) -> Callable[
        [contact_center_insights.ListConversationsRequest],
        contact_center_insights.ListConversationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConversations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_issue_models(
        self,
    ) -> Callable[
        [contact_center_insights.ListIssueModelsRequest],
        contact_center_insights.ListIssueModelsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListIssueModels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_issues(
        self,
    ) -> Callable[
        [contact_center_insights.ListIssuesRequest],
        contact_center_insights.ListIssuesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListIssues(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_phrase_matchers(
        self,
    ) -> Callable[
        [contact_center_insights.ListPhraseMatchersRequest],
        contact_center_insights.ListPhraseMatchersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPhraseMatchers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_views(
        self,
    ) -> Callable[
        [contact_center_insights.ListViewsRequest],
        contact_center_insights.ListViewsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListViews(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undeploy_issue_model(
        self,
    ) -> Callable[
        [contact_center_insights.UndeployIssueModelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeployIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_conversation(
        self,
    ) -> Callable[
        [contact_center_insights.UpdateConversationRequest], resources.Conversation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_issue(
        self,
    ) -> Callable[[contact_center_insights.UpdateIssueRequest], resources.Issue]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateIssue(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_issue_model(
        self,
    ) -> Callable[
        [contact_center_insights.UpdateIssueModelRequest], resources.IssueModel
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateIssueModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_phrase_matcher(
        self,
    ) -> Callable[
        [contact_center_insights.UpdatePhraseMatcherRequest], resources.PhraseMatcher
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePhraseMatcher(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_settings(
        self,
    ) -> Callable[[contact_center_insights.UpdateSettingsRequest], resources.Settings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_view(
        self,
    ) -> Callable[[contact_center_insights.UpdateViewRequest], resources.View]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateView(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def upload_conversation(
        self,
    ) -> Callable[
        [contact_center_insights.UploadConversationRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UploadConversation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseContactCenterInsightsRestTransport._BaseCancelOperation,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.CancelOperation")

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
                _BaseContactCenterInsightsRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ContactCenterInsightsRestTransport._CancelOperation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseContactCenterInsightsRestTransport._BaseGetOperation,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.GetOperation")

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
                _BaseContactCenterInsightsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._GetOperation._get_response(
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
        _BaseContactCenterInsightsRestTransport._BaseListOperations,
        ContactCenterInsightsRestStub,
    ):
        def __hash__(self):
            return hash("ContactCenterInsightsRestTransport.ListOperations")

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
                _BaseContactCenterInsightsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseContactCenterInsightsRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContactCenterInsightsRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ContactCenterInsightsRestTransport._ListOperations._get_response(
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


__all__ = ("ContactCenterInsightsRestTransport",)
