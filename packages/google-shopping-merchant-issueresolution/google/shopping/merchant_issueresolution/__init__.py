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
from google.shopping.merchant_issueresolution import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_issueresolution_v1beta.services.aggregate_product_statuses_service.async_client import (
    AggregateProductStatusesServiceAsyncClient,
)
from google.shopping.merchant_issueresolution_v1beta.services.aggregate_product_statuses_service.client import (
    AggregateProductStatusesServiceClient,
)
from google.shopping.merchant_issueresolution_v1beta.services.issue_resolution_service.async_client import (
    IssueResolutionServiceAsyncClient,
)
from google.shopping.merchant_issueresolution_v1beta.services.issue_resolution_service.client import (
    IssueResolutionServiceClient,
)
from google.shopping.merchant_issueresolution_v1beta.types.aggregateproductstatuses import (
    AggregateProductStatus,
    ListAggregateProductStatusesRequest,
    ListAggregateProductStatusesResponse,
)
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import (
    Action,
    ActionFlow,
    ActionInput,
    Breakdown,
    BuiltInSimpleAction,
    BuiltInUserInputAction,
    Callout,
    ContentOption,
    ExternalAction,
    Impact,
    InputField,
    InputValue,
    RenderAccountIssuesRequest,
    RenderAccountIssuesResponse,
    RenderedIssue,
    RenderIssuesRequestPayload,
    RenderProductIssuesRequest,
    RenderProductIssuesResponse,
    Severity,
    TextWithTooltip,
    TriggerActionPayload,
    TriggerActionRequest,
    TriggerActionResponse,
    UserInputActionRenderingOption,
)

__all__ = (
    "AggregateProductStatusesServiceClient",
    "AggregateProductStatusesServiceAsyncClient",
    "IssueResolutionServiceClient",
    "IssueResolutionServiceAsyncClient",
    "AggregateProductStatus",
    "ListAggregateProductStatusesRequest",
    "ListAggregateProductStatusesResponse",
    "Action",
    "ActionFlow",
    "ActionInput",
    "Breakdown",
    "BuiltInSimpleAction",
    "BuiltInUserInputAction",
    "Callout",
    "ExternalAction",
    "Impact",
    "InputField",
    "InputValue",
    "RenderAccountIssuesRequest",
    "RenderAccountIssuesResponse",
    "RenderedIssue",
    "RenderIssuesRequestPayload",
    "RenderProductIssuesRequest",
    "RenderProductIssuesResponse",
    "TextWithTooltip",
    "TriggerActionPayload",
    "TriggerActionRequest",
    "TriggerActionResponse",
    "ContentOption",
    "Severity",
    "UserInputActionRenderingOption",
)
