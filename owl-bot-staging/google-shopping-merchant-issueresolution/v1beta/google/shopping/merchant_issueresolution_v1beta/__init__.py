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
from google.shopping.merchant_issueresolution_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.aggregate_product_statuses_service import AggregateProductStatusesServiceClient
from .services.aggregate_product_statuses_service import AggregateProductStatusesServiceAsyncClient
from .services.issue_resolution_service import IssueResolutionServiceClient
from .services.issue_resolution_service import IssueResolutionServiceAsyncClient

from .types.aggregateproductstatuses import AggregateProductStatus
from .types.aggregateproductstatuses import ListAggregateProductStatusesRequest
from .types.aggregateproductstatuses import ListAggregateProductStatusesResponse
from .types.issueresolution import Action
from .types.issueresolution import ActionFlow
from .types.issueresolution import ActionInput
from .types.issueresolution import Breakdown
from .types.issueresolution import BuiltInSimpleAction
from .types.issueresolution import BuiltInUserInputAction
from .types.issueresolution import Callout
from .types.issueresolution import ExternalAction
from .types.issueresolution import Impact
from .types.issueresolution import InputField
from .types.issueresolution import InputValue
from .types.issueresolution import RenderAccountIssuesRequest
from .types.issueresolution import RenderAccountIssuesResponse
from .types.issueresolution import RenderedIssue
from .types.issueresolution import RenderIssuesRequestPayload
from .types.issueresolution import RenderProductIssuesRequest
from .types.issueresolution import RenderProductIssuesResponse
from .types.issueresolution import TextWithTooltip
from .types.issueresolution import TriggerActionPayload
from .types.issueresolution import TriggerActionRequest
from .types.issueresolution import TriggerActionResponse
from .types.issueresolution import ContentOption
from .types.issueresolution import Severity
from .types.issueresolution import UserInputActionRenderingOption

__all__ = (
    'AggregateProductStatusesServiceAsyncClient',
    'IssueResolutionServiceAsyncClient',
'Action',
'ActionFlow',
'ActionInput',
'AggregateProductStatus',
'AggregateProductStatusesServiceClient',
'Breakdown',
'BuiltInSimpleAction',
'BuiltInUserInputAction',
'Callout',
'ContentOption',
'ExternalAction',
'Impact',
'InputField',
'InputValue',
'IssueResolutionServiceClient',
'ListAggregateProductStatusesRequest',
'ListAggregateProductStatusesResponse',
'RenderAccountIssuesRequest',
'RenderAccountIssuesResponse',
'RenderIssuesRequestPayload',
'RenderProductIssuesRequest',
'RenderProductIssuesResponse',
'RenderedIssue',
'Severity',
'TextWithTooltip',
'TriggerActionPayload',
'TriggerActionRequest',
'TriggerActionResponse',
'UserInputActionRenderingOption',
)
