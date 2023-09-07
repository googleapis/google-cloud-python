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
from google.cloud.channel_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_channel_reports_service import CloudChannelReportsServiceClient
from .services.cloud_channel_reports_service import CloudChannelReportsServiceAsyncClient
from .services.cloud_channel_service import CloudChannelServiceClient
from .services.cloud_channel_service import CloudChannelServiceAsyncClient

from .types.billing_accounts import BillingAccount
from .types.channel_partner_links import ChannelPartnerLink
from .types.channel_partner_links import ChannelPartnerLinkState
from .types.channel_partner_links import ChannelPartnerLinkView
from .types.common import AdminUser
from .types.common import CloudIdentityInfo
from .types.common import EduData
from .types.common import Value
from .types.customers import ContactInfo
from .types.customers import Customer
from .types.entitlement_changes import EntitlementChange
from .types.entitlements import AssociationInfo
from .types.entitlements import CommitmentSettings
from .types.entitlements import Entitlement
from .types.entitlements import Parameter
from .types.entitlements import ProvisionedService
from .types.entitlements import RenewalSettings
from .types.entitlements import TransferableSku
from .types.entitlements import TransferEligibility
from .types.entitlements import TrialSettings
from .types.offers import Constraints
from .types.offers import CustomerConstraints
from .types.offers import Offer
from .types.offers import ParameterDefinition
from .types.offers import Period
from .types.offers import Plan
from .types.offers import Price
from .types.offers import PriceByResource
from .types.offers import PricePhase
from .types.offers import PriceTier
from .types.offers import PaymentPlan
from .types.offers import PaymentType
from .types.offers import PeriodType
from .types.offers import PromotionalOrderType
from .types.offers import ResourceType
from .types.operations import OperationMetadata
from .types.products import MarketingInfo
from .types.products import Media
from .types.products import Product
from .types.products import Sku
from .types.products import MediaType
from .types.reports_service import Column
from .types.reports_service import DateRange
from .types.reports_service import FetchReportResultsRequest
from .types.reports_service import FetchReportResultsResponse
from .types.reports_service import ListReportsRequest
from .types.reports_service import ListReportsResponse
from .types.reports_service import Report
from .types.reports_service import ReportJob
from .types.reports_service import ReportResultsMetadata
from .types.reports_service import ReportStatus
from .types.reports_service import ReportValue
from .types.reports_service import Row
from .types.reports_service import RunReportJobRequest
from .types.reports_service import RunReportJobResponse
from .types.repricing import ChannelPartnerRepricingConfig
from .types.repricing import ConditionalOverride
from .types.repricing import CustomerRepricingConfig
from .types.repricing import PercentageAdjustment
from .types.repricing import RepricingAdjustment
from .types.repricing import RepricingCondition
from .types.repricing import RepricingConfig
from .types.repricing import SkuGroupCondition
from .types.repricing import RebillingBasis
from .types.service import ActivateEntitlementRequest
from .types.service import BillableSku
from .types.service import BillingAccountPurchaseInfo
from .types.service import CancelEntitlementRequest
from .types.service import ChangeOfferRequest
from .types.service import ChangeParametersRequest
from .types.service import ChangeRenewalSettingsRequest
from .types.service import CheckCloudIdentityAccountsExistRequest
from .types.service import CheckCloudIdentityAccountsExistResponse
from .types.service import CloudIdentityCustomerAccount
from .types.service import CreateChannelPartnerLinkRequest
from .types.service import CreateChannelPartnerRepricingConfigRequest
from .types.service import CreateCustomerRepricingConfigRequest
from .types.service import CreateCustomerRequest
from .types.service import CreateEntitlementRequest
from .types.service import DeleteChannelPartnerRepricingConfigRequest
from .types.service import DeleteCustomerRepricingConfigRequest
from .types.service import DeleteCustomerRequest
from .types.service import GetChannelPartnerLinkRequest
from .types.service import GetChannelPartnerRepricingConfigRequest
from .types.service import GetCustomerRepricingConfigRequest
from .types.service import GetCustomerRequest
from .types.service import GetEntitlementRequest
from .types.service import ImportCustomerRequest
from .types.service import ListChannelPartnerLinksRequest
from .types.service import ListChannelPartnerLinksResponse
from .types.service import ListChannelPartnerRepricingConfigsRequest
from .types.service import ListChannelPartnerRepricingConfigsResponse
from .types.service import ListCustomerRepricingConfigsRequest
from .types.service import ListCustomerRepricingConfigsResponse
from .types.service import ListCustomersRequest
from .types.service import ListCustomersResponse
from .types.service import ListEntitlementChangesRequest
from .types.service import ListEntitlementChangesResponse
from .types.service import ListEntitlementsRequest
from .types.service import ListEntitlementsResponse
from .types.service import ListOffersRequest
from .types.service import ListOffersResponse
from .types.service import ListProductsRequest
from .types.service import ListProductsResponse
from .types.service import ListPurchasableOffersRequest
from .types.service import ListPurchasableOffersResponse
from .types.service import ListPurchasableSkusRequest
from .types.service import ListPurchasableSkusResponse
from .types.service import ListSkuGroupBillableSkusRequest
from .types.service import ListSkuGroupBillableSkusResponse
from .types.service import ListSkuGroupsRequest
from .types.service import ListSkuGroupsResponse
from .types.service import ListSkusRequest
from .types.service import ListSkusResponse
from .types.service import ListSubscribersRequest
from .types.service import ListSubscribersResponse
from .types.service import ListTransferableOffersRequest
from .types.service import ListTransferableOffersResponse
from .types.service import ListTransferableSkusRequest
from .types.service import ListTransferableSkusResponse
from .types.service import LookupOfferRequest
from .types.service import ProvisionCloudIdentityRequest
from .types.service import PurchasableOffer
from .types.service import PurchasableSku
from .types.service import QueryEligibleBillingAccountsRequest
from .types.service import QueryEligibleBillingAccountsResponse
from .types.service import RegisterSubscriberRequest
from .types.service import RegisterSubscriberResponse
from .types.service import SkuGroup
from .types.service import SkuPurchaseGroup
from .types.service import StartPaidServiceRequest
from .types.service import SuspendEntitlementRequest
from .types.service import TransferableOffer
from .types.service import TransferEntitlementsRequest
from .types.service import TransferEntitlementsResponse
from .types.service import TransferEntitlementsToGoogleRequest
from .types.service import UnregisterSubscriberRequest
from .types.service import UnregisterSubscriberResponse
from .types.service import UpdateChannelPartnerLinkRequest
from .types.service import UpdateChannelPartnerRepricingConfigRequest
from .types.service import UpdateCustomerRepricingConfigRequest
from .types.service import UpdateCustomerRequest
from .types.subscriber_event import CustomerEvent
from .types.subscriber_event import EntitlementEvent
from .types.subscriber_event import SubscriberEvent

__all__ = (
    'CloudChannelReportsServiceAsyncClient',
    'CloudChannelServiceAsyncClient',
'ActivateEntitlementRequest',
'AdminUser',
'AssociationInfo',
'BillableSku',
'BillingAccount',
'BillingAccountPurchaseInfo',
'CancelEntitlementRequest',
'ChangeOfferRequest',
'ChangeParametersRequest',
'ChangeRenewalSettingsRequest',
'ChannelPartnerLink',
'ChannelPartnerLinkState',
'ChannelPartnerLinkView',
'ChannelPartnerRepricingConfig',
'CheckCloudIdentityAccountsExistRequest',
'CheckCloudIdentityAccountsExistResponse',
'CloudChannelReportsServiceClient',
'CloudChannelServiceClient',
'CloudIdentityCustomerAccount',
'CloudIdentityInfo',
'Column',
'CommitmentSettings',
'ConditionalOverride',
'Constraints',
'ContactInfo',
'CreateChannelPartnerLinkRequest',
'CreateChannelPartnerRepricingConfigRequest',
'CreateCustomerRepricingConfigRequest',
'CreateCustomerRequest',
'CreateEntitlementRequest',
'Customer',
'CustomerConstraints',
'CustomerEvent',
'CustomerRepricingConfig',
'DateRange',
'DeleteChannelPartnerRepricingConfigRequest',
'DeleteCustomerRepricingConfigRequest',
'DeleteCustomerRequest',
'EduData',
'Entitlement',
'EntitlementChange',
'EntitlementEvent',
'FetchReportResultsRequest',
'FetchReportResultsResponse',
'GetChannelPartnerLinkRequest',
'GetChannelPartnerRepricingConfigRequest',
'GetCustomerRepricingConfigRequest',
'GetCustomerRequest',
'GetEntitlementRequest',
'ImportCustomerRequest',
'ListChannelPartnerLinksRequest',
'ListChannelPartnerLinksResponse',
'ListChannelPartnerRepricingConfigsRequest',
'ListChannelPartnerRepricingConfigsResponse',
'ListCustomerRepricingConfigsRequest',
'ListCustomerRepricingConfigsResponse',
'ListCustomersRequest',
'ListCustomersResponse',
'ListEntitlementChangesRequest',
'ListEntitlementChangesResponse',
'ListEntitlementsRequest',
'ListEntitlementsResponse',
'ListOffersRequest',
'ListOffersResponse',
'ListProductsRequest',
'ListProductsResponse',
'ListPurchasableOffersRequest',
'ListPurchasableOffersResponse',
'ListPurchasableSkusRequest',
'ListPurchasableSkusResponse',
'ListReportsRequest',
'ListReportsResponse',
'ListSkuGroupBillableSkusRequest',
'ListSkuGroupBillableSkusResponse',
'ListSkuGroupsRequest',
'ListSkuGroupsResponse',
'ListSkusRequest',
'ListSkusResponse',
'ListSubscribersRequest',
'ListSubscribersResponse',
'ListTransferableOffersRequest',
'ListTransferableOffersResponse',
'ListTransferableSkusRequest',
'ListTransferableSkusResponse',
'LookupOfferRequest',
'MarketingInfo',
'Media',
'MediaType',
'Offer',
'OperationMetadata',
'Parameter',
'ParameterDefinition',
'PaymentPlan',
'PaymentType',
'PercentageAdjustment',
'Period',
'PeriodType',
'Plan',
'Price',
'PriceByResource',
'PricePhase',
'PriceTier',
'Product',
'PromotionalOrderType',
'ProvisionCloudIdentityRequest',
'ProvisionedService',
'PurchasableOffer',
'PurchasableSku',
'QueryEligibleBillingAccountsRequest',
'QueryEligibleBillingAccountsResponse',
'RebillingBasis',
'RegisterSubscriberRequest',
'RegisterSubscriberResponse',
'RenewalSettings',
'Report',
'ReportJob',
'ReportResultsMetadata',
'ReportStatus',
'ReportValue',
'RepricingAdjustment',
'RepricingCondition',
'RepricingConfig',
'ResourceType',
'Row',
'RunReportJobRequest',
'RunReportJobResponse',
'Sku',
'SkuGroup',
'SkuGroupCondition',
'SkuPurchaseGroup',
'StartPaidServiceRequest',
'SubscriberEvent',
'SuspendEntitlementRequest',
'TransferEligibility',
'TransferEntitlementsRequest',
'TransferEntitlementsResponse',
'TransferEntitlementsToGoogleRequest',
'TransferableOffer',
'TransferableSku',
'TrialSettings',
'UnregisterSubscriberRequest',
'UnregisterSubscriberResponse',
'UpdateChannelPartnerLinkRequest',
'UpdateChannelPartnerRepricingConfigRequest',
'UpdateCustomerRepricingConfigRequest',
'UpdateCustomerRequest',
'Value',
)
