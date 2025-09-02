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


from google.shopping.merchant_issueresolution_v1beta.services.aggregate_product_statuses_service.client import AggregateProductStatusesServiceClient
from google.shopping.merchant_issueresolution_v1beta.services.aggregate_product_statuses_service.async_client import AggregateProductStatusesServiceAsyncClient
from google.shopping.merchant_issueresolution_v1beta.services.issue_resolution_service.client import IssueResolutionServiceClient
from google.shopping.merchant_issueresolution_v1beta.services.issue_resolution_service.async_client import IssueResolutionServiceAsyncClient

from google.shopping.merchant_issueresolution_v1beta.types.aggregateproductstatuses import AggregateProductStatus
from google.shopping.merchant_issueresolution_v1beta.types.aggregateproductstatuses import ListAggregateProductStatusesRequest
from google.shopping.merchant_issueresolution_v1beta.types.aggregateproductstatuses import ListAggregateProductStatusesResponse
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import Action
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import ActionFlow
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import ActionInput
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import Breakdown
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import BuiltInSimpleAction
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import BuiltInUserInputAction
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import Callout
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import ExternalAction
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import Impact
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import InputField
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import InputValue
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import RenderAccountIssuesRequest
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import RenderAccountIssuesResponse
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import RenderedIssue
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import RenderIssuesRequestPayload
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import RenderProductIssuesRequest
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import RenderProductIssuesResponse
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import TextWithTooltip
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import TriggerActionPayload
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import TriggerActionRequest
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import TriggerActionResponse
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import ContentOption
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import Severity
from google.shopping.merchant_issueresolution_v1beta.types.issueresolution import UserInputActionRenderingOption

__all__ = ('AggregateProductStatusesServiceClient',
    'AggregateProductStatusesServiceAsyncClient',
    'IssueResolutionServiceClient',
    'IssueResolutionServiceAsyncClient',
    'AggregateProductStatus',
    'ListAggregateProductStatusesRequest',
    'ListAggregateProductStatusesResponse',
    'Action',
    'ActionFlow',
    'ActionInput',
    'Breakdown',
    'BuiltInSimpleAction',
    'BuiltInUserInputAction',
    'Callout',
    'ExternalAction',
    'Impact',
    'InputField',
    'InputValue',
    'RenderAccountIssuesRequest',
    'RenderAccountIssuesResponse',
    'RenderedIssue',
    'RenderIssuesRequestPayload',
    'RenderProductIssuesRequest',
    'RenderProductIssuesResponse',
    'TextWithTooltip',
    'TriggerActionPayload',
    'TriggerActionRequest',
    'TriggerActionResponse',
    'ContentOption',
    'Severity',
    'UserInputActionRenderingOption',
)
