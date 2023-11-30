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
from google.cloud.channel import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.channel_v1.services.cloud_channel_reports_service.client import CloudChannelReportsServiceClient
from google.cloud.channel_v1.services.cloud_channel_reports_service.async_client import CloudChannelReportsServiceAsyncClient
from google.cloud.channel_v1.services.cloud_channel_service.client import CloudChannelServiceClient
from google.cloud.channel_v1.services.cloud_channel_service.async_client import CloudChannelServiceAsyncClient

from google.cloud.channel_v1.types.billing_accounts import BillingAccount
from google.cloud.channel_v1.types.channel_partner_links import ChannelPartnerLink
from google.cloud.channel_v1.types.channel_partner_links import ChannelPartnerLinkState
from google.cloud.channel_v1.types.channel_partner_links import ChannelPartnerLinkView
from google.cloud.channel_v1.types.common import AdminUser
from google.cloud.channel_v1.types.common import CloudIdentityInfo
from google.cloud.channel_v1.types.common import EduData
from google.cloud.channel_v1.types.common import Value
from google.cloud.channel_v1.types.customers import ContactInfo
from google.cloud.channel_v1.types.customers import Customer
from google.cloud.channel_v1.types.entitlement_changes import EntitlementChange
from google.cloud.channel_v1.types.entitlements import AssociationInfo
from google.cloud.channel_v1.types.entitlements import CommitmentSettings
from google.cloud.channel_v1.types.entitlements import Entitlement
from google.cloud.channel_v1.types.entitlements import Parameter
from google.cloud.channel_v1.types.entitlements import ProvisionedService
from google.cloud.channel_v1.types.entitlements import RenewalSettings
from google.cloud.channel_v1.types.entitlements import TransferableSku
from google.cloud.channel_v1.types.entitlements import TransferEligibility
from google.cloud.channel_v1.types.entitlements import TrialSettings
from google.cloud.channel_v1.types.offers import Constraints
from google.cloud.channel_v1.types.offers import CustomerConstraints
from google.cloud.channel_v1.types.offers import Offer
from google.cloud.channel_v1.types.offers import ParameterDefinition
from google.cloud.channel_v1.types.offers import Period
from google.cloud.channel_v1.types.offers import Plan
from google.cloud.channel_v1.types.offers import Price
from google.cloud.channel_v1.types.offers import PriceByResource
from google.cloud.channel_v1.types.offers import PricePhase
from google.cloud.channel_v1.types.offers import PriceTier
from google.cloud.channel_v1.types.offers import PaymentPlan
from google.cloud.channel_v1.types.offers import PaymentType
from google.cloud.channel_v1.types.offers import PeriodType
from google.cloud.channel_v1.types.offers import PromotionalOrderType
from google.cloud.channel_v1.types.offers import ResourceType
from google.cloud.channel_v1.types.operations import OperationMetadata
from google.cloud.channel_v1.types.products import MarketingInfo
from google.cloud.channel_v1.types.products import Media
from google.cloud.channel_v1.types.products import Product
from google.cloud.channel_v1.types.products import Sku
from google.cloud.channel_v1.types.products import MediaType
from google.cloud.channel_v1.types.reports_service import Column
from google.cloud.channel_v1.types.reports_service import DateRange
from google.cloud.channel_v1.types.reports_service import FetchReportResultsRequest
from google.cloud.channel_v1.types.reports_service import FetchReportResultsResponse
from google.cloud.channel_v1.types.reports_service import ListReportsRequest
from google.cloud.channel_v1.types.reports_service import ListReportsResponse
from google.cloud.channel_v1.types.reports_service import Report
from google.cloud.channel_v1.types.reports_service import ReportJob
from google.cloud.channel_v1.types.reports_service import ReportResultsMetadata
from google.cloud.channel_v1.types.reports_service import ReportStatus
from google.cloud.channel_v1.types.reports_service import ReportValue
from google.cloud.channel_v1.types.reports_service import Row
from google.cloud.channel_v1.types.reports_service import RunReportJobRequest
from google.cloud.channel_v1.types.reports_service import RunReportJobResponse
from google.cloud.channel_v1.types.repricing import ChannelPartnerRepricingConfig
from google.cloud.channel_v1.types.repricing import ConditionalOverride
from google.cloud.channel_v1.types.repricing import CustomerRepricingConfig
from google.cloud.channel_v1.types.repricing import PercentageAdjustment
from google.cloud.channel_v1.types.repricing import RepricingAdjustment
from google.cloud.channel_v1.types.repricing import RepricingCondition
from google.cloud.channel_v1.types.repricing import RepricingConfig
from google.cloud.channel_v1.types.repricing import SkuGroupCondition
from google.cloud.channel_v1.types.repricing import RebillingBasis
from google.cloud.channel_v1.types.service import ActivateEntitlementRequest
from google.cloud.channel_v1.types.service import BillableSku
from google.cloud.channel_v1.types.service import BillingAccountPurchaseInfo
from google.cloud.channel_v1.types.service import CancelEntitlementRequest
from google.cloud.channel_v1.types.service import ChangeOfferRequest
from google.cloud.channel_v1.types.service import ChangeParametersRequest
from google.cloud.channel_v1.types.service import ChangeRenewalSettingsRequest
from google.cloud.channel_v1.types.service import CheckCloudIdentityAccountsExistRequest
from google.cloud.channel_v1.types.service import CheckCloudIdentityAccountsExistResponse
from google.cloud.channel_v1.types.service import CloudIdentityCustomerAccount
from google.cloud.channel_v1.types.service import CreateChannelPartnerLinkRequest
from google.cloud.channel_v1.types.service import CreateChannelPartnerRepricingConfigRequest
from google.cloud.channel_v1.types.service import CreateCustomerRepricingConfigRequest
from google.cloud.channel_v1.types.service import CreateCustomerRequest
from google.cloud.channel_v1.types.service import CreateEntitlementRequest
from google.cloud.channel_v1.types.service import DeleteChannelPartnerRepricingConfigRequest
from google.cloud.channel_v1.types.service import DeleteCustomerRepricingConfigRequest
from google.cloud.channel_v1.types.service import DeleteCustomerRequest
from google.cloud.channel_v1.types.service import GetChannelPartnerLinkRequest
from google.cloud.channel_v1.types.service import GetChannelPartnerRepricingConfigRequest
from google.cloud.channel_v1.types.service import GetCustomerRepricingConfigRequest
from google.cloud.channel_v1.types.service import GetCustomerRequest
from google.cloud.channel_v1.types.service import GetEntitlementRequest
from google.cloud.channel_v1.types.service import ImportCustomerRequest
from google.cloud.channel_v1.types.service import ListChannelPartnerLinksRequest
from google.cloud.channel_v1.types.service import ListChannelPartnerLinksResponse
from google.cloud.channel_v1.types.service import ListChannelPartnerRepricingConfigsRequest
from google.cloud.channel_v1.types.service import ListChannelPartnerRepricingConfigsResponse
from google.cloud.channel_v1.types.service import ListCustomerRepricingConfigsRequest
from google.cloud.channel_v1.types.service import ListCustomerRepricingConfigsResponse
from google.cloud.channel_v1.types.service import ListCustomersRequest
from google.cloud.channel_v1.types.service import ListCustomersResponse
from google.cloud.channel_v1.types.service import ListEntitlementChangesRequest
from google.cloud.channel_v1.types.service import ListEntitlementChangesResponse
from google.cloud.channel_v1.types.service import ListEntitlementsRequest
from google.cloud.channel_v1.types.service import ListEntitlementsResponse
from google.cloud.channel_v1.types.service import ListOffersRequest
from google.cloud.channel_v1.types.service import ListOffersResponse
from google.cloud.channel_v1.types.service import ListProductsRequest
from google.cloud.channel_v1.types.service import ListProductsResponse
from google.cloud.channel_v1.types.service import ListPurchasableOffersRequest
from google.cloud.channel_v1.types.service import ListPurchasableOffersResponse
from google.cloud.channel_v1.types.service import ListPurchasableSkusRequest
from google.cloud.channel_v1.types.service import ListPurchasableSkusResponse
from google.cloud.channel_v1.types.service import ListSkuGroupBillableSkusRequest
from google.cloud.channel_v1.types.service import ListSkuGroupBillableSkusResponse
from google.cloud.channel_v1.types.service import ListSkuGroupsRequest
from google.cloud.channel_v1.types.service import ListSkuGroupsResponse
from google.cloud.channel_v1.types.service import ListSkusRequest
from google.cloud.channel_v1.types.service import ListSkusResponse
from google.cloud.channel_v1.types.service import ListSubscribersRequest
from google.cloud.channel_v1.types.service import ListSubscribersResponse
from google.cloud.channel_v1.types.service import ListTransferableOffersRequest
from google.cloud.channel_v1.types.service import ListTransferableOffersResponse
from google.cloud.channel_v1.types.service import ListTransferableSkusRequest
from google.cloud.channel_v1.types.service import ListTransferableSkusResponse
from google.cloud.channel_v1.types.service import LookupOfferRequest
from google.cloud.channel_v1.types.service import ProvisionCloudIdentityRequest
from google.cloud.channel_v1.types.service import PurchasableOffer
from google.cloud.channel_v1.types.service import PurchasableSku
from google.cloud.channel_v1.types.service import QueryEligibleBillingAccountsRequest
from google.cloud.channel_v1.types.service import QueryEligibleBillingAccountsResponse
from google.cloud.channel_v1.types.service import RegisterSubscriberRequest
from google.cloud.channel_v1.types.service import RegisterSubscriberResponse
from google.cloud.channel_v1.types.service import SkuGroup
from google.cloud.channel_v1.types.service import SkuPurchaseGroup
from google.cloud.channel_v1.types.service import StartPaidServiceRequest
from google.cloud.channel_v1.types.service import SuspendEntitlementRequest
from google.cloud.channel_v1.types.service import TransferableOffer
from google.cloud.channel_v1.types.service import TransferEntitlementsRequest
from google.cloud.channel_v1.types.service import TransferEntitlementsResponse
from google.cloud.channel_v1.types.service import TransferEntitlementsToGoogleRequest
from google.cloud.channel_v1.types.service import UnregisterSubscriberRequest
from google.cloud.channel_v1.types.service import UnregisterSubscriberResponse
from google.cloud.channel_v1.types.service import UpdateChannelPartnerLinkRequest
from google.cloud.channel_v1.types.service import UpdateChannelPartnerRepricingConfigRequest
from google.cloud.channel_v1.types.service import UpdateCustomerRepricingConfigRequest
from google.cloud.channel_v1.types.service import UpdateCustomerRequest
from google.cloud.channel_v1.types.subscriber_event import CustomerEvent
from google.cloud.channel_v1.types.subscriber_event import EntitlementEvent
from google.cloud.channel_v1.types.subscriber_event import SubscriberEvent

__all__ = ('CloudChannelReportsServiceClient',
    'CloudChannelReportsServiceAsyncClient',
    'CloudChannelServiceClient',
    'CloudChannelServiceAsyncClient',
    'BillingAccount',
    'ChannelPartnerLink',
    'ChannelPartnerLinkState',
    'ChannelPartnerLinkView',
    'AdminUser',
    'CloudIdentityInfo',
    'EduData',
    'Value',
    'ContactInfo',
    'Customer',
    'EntitlementChange',
    'AssociationInfo',
    'CommitmentSettings',
    'Entitlement',
    'Parameter',
    'ProvisionedService',
    'RenewalSettings',
    'TransferableSku',
    'TransferEligibility',
    'TrialSettings',
    'Constraints',
    'CustomerConstraints',
    'Offer',
    'ParameterDefinition',
    'Period',
    'Plan',
    'Price',
    'PriceByResource',
    'PricePhase',
    'PriceTier',
    'PaymentPlan',
    'PaymentType',
    'PeriodType',
    'PromotionalOrderType',
    'ResourceType',
    'OperationMetadata',
    'MarketingInfo',
    'Media',
    'Product',
    'Sku',
    'MediaType',
    'Column',
    'DateRange',
    'FetchReportResultsRequest',
    'FetchReportResultsResponse',
    'ListReportsRequest',
    'ListReportsResponse',
    'Report',
    'ReportJob',
    'ReportResultsMetadata',
    'ReportStatus',
    'ReportValue',
    'Row',
    'RunReportJobRequest',
    'RunReportJobResponse',
    'ChannelPartnerRepricingConfig',
    'ConditionalOverride',
    'CustomerRepricingConfig',
    'PercentageAdjustment',
    'RepricingAdjustment',
    'RepricingCondition',
    'RepricingConfig',
    'SkuGroupCondition',
    'RebillingBasis',
    'ActivateEntitlementRequest',
    'BillableSku',
    'BillingAccountPurchaseInfo',
    'CancelEntitlementRequest',
    'ChangeOfferRequest',
    'ChangeParametersRequest',
    'ChangeRenewalSettingsRequest',
    'CheckCloudIdentityAccountsExistRequest',
    'CheckCloudIdentityAccountsExistResponse',
    'CloudIdentityCustomerAccount',
    'CreateChannelPartnerLinkRequest',
    'CreateChannelPartnerRepricingConfigRequest',
    'CreateCustomerRepricingConfigRequest',
    'CreateCustomerRequest',
    'CreateEntitlementRequest',
    'DeleteChannelPartnerRepricingConfigRequest',
    'DeleteCustomerRepricingConfigRequest',
    'DeleteCustomerRequest',
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
    'ProvisionCloudIdentityRequest',
    'PurchasableOffer',
    'PurchasableSku',
    'QueryEligibleBillingAccountsRequest',
    'QueryEligibleBillingAccountsResponse',
    'RegisterSubscriberRequest',
    'RegisterSubscriberResponse',
    'SkuGroup',
    'SkuPurchaseGroup',
    'StartPaidServiceRequest',
    'SuspendEntitlementRequest',
    'TransferableOffer',
    'TransferEntitlementsRequest',
    'TransferEntitlementsResponse',
    'TransferEntitlementsToGoogleRequest',
    'UnregisterSubscriberRequest',
    'UnregisterSubscriberResponse',
    'UpdateChannelPartnerLinkRequest',
    'UpdateChannelPartnerRepricingConfigRequest',
    'UpdateCustomerRepricingConfigRequest',
    'UpdateCustomerRequest',
    'CustomerEvent',
    'EntitlementEvent',
    'SubscriberEvent',
)
