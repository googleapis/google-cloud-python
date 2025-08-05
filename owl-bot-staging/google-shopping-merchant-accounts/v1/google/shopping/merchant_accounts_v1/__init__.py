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
from google.shopping.merchant_accounts_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.account_issue_service import AccountIssueServiceClient
from .services.account_issue_service import AccountIssueServiceAsyncClient
from .services.account_relationships_service import AccountRelationshipsServiceClient
from .services.account_relationships_service import AccountRelationshipsServiceAsyncClient
from .services.account_services_service import AccountServicesServiceClient
from .services.account_services_service import AccountServicesServiceAsyncClient
from .services.accounts_service import AccountsServiceClient
from .services.accounts_service import AccountsServiceAsyncClient
from .services.autofeed_settings_service import AutofeedSettingsServiceClient
from .services.autofeed_settings_service import AutofeedSettingsServiceAsyncClient
from .services.automatic_improvements_service import AutomaticImprovementsServiceClient
from .services.automatic_improvements_service import AutomaticImprovementsServiceAsyncClient
from .services.business_identity_service import BusinessIdentityServiceClient
from .services.business_identity_service import BusinessIdentityServiceAsyncClient
from .services.business_info_service import BusinessInfoServiceClient
from .services.business_info_service import BusinessInfoServiceAsyncClient
from .services.checkout_settings_service import CheckoutSettingsServiceClient
from .services.checkout_settings_service import CheckoutSettingsServiceAsyncClient
from .services.developer_registration_service import DeveloperRegistrationServiceClient
from .services.developer_registration_service import DeveloperRegistrationServiceAsyncClient
from .services.email_preferences_service import EmailPreferencesServiceClient
from .services.email_preferences_service import EmailPreferencesServiceAsyncClient
from .services.gbp_accounts_service import GbpAccountsServiceClient
from .services.gbp_accounts_service import GbpAccountsServiceAsyncClient
from .services.homepage_service import HomepageServiceClient
from .services.homepage_service import HomepageServiceAsyncClient
from .services.lfp_providers_service import LfpProvidersServiceClient
from .services.lfp_providers_service import LfpProvidersServiceAsyncClient
from .services.omnichannel_settings_service import OmnichannelSettingsServiceClient
from .services.omnichannel_settings_service import OmnichannelSettingsServiceAsyncClient
from .services.online_return_policy_service import OnlineReturnPolicyServiceClient
from .services.online_return_policy_service import OnlineReturnPolicyServiceAsyncClient
from .services.programs_service import ProgramsServiceClient
from .services.programs_service import ProgramsServiceAsyncClient
from .services.regions_service import RegionsServiceClient
from .services.regions_service import RegionsServiceAsyncClient
from .services.shipping_settings_service import ShippingSettingsServiceClient
from .services.shipping_settings_service import ShippingSettingsServiceAsyncClient
from .services.terms_of_service_agreement_state_service import TermsOfServiceAgreementStateServiceClient
from .services.terms_of_service_agreement_state_service import TermsOfServiceAgreementStateServiceAsyncClient
from .services.terms_of_service_service import TermsOfServiceServiceClient
from .services.terms_of_service_service import TermsOfServiceServiceAsyncClient
from .services.user_service import UserServiceClient
from .services.user_service import UserServiceAsyncClient

from .types.accessright import AccessRight
from .types.accountissue import AccountIssue
from .types.accountissue import ListAccountIssuesRequest
from .types.accountissue import ListAccountIssuesResponse
from .types.accountrelationships import AccountRelationship
from .types.accountrelationships import GetAccountRelationshipRequest
from .types.accountrelationships import ListAccountRelationshipsRequest
from .types.accountrelationships import ListAccountRelationshipsResponse
from .types.accountrelationships import UpdateAccountRelationshipRequest
from .types.accounts import Account
from .types.accounts import CreateAndConfigureAccountRequest
from .types.accounts import DeleteAccountRequest
from .types.accounts import GetAccountRequest
from .types.accounts import ListAccountsRequest
from .types.accounts import ListAccountsResponse
from .types.accounts import ListSubAccountsRequest
from .types.accounts import ListSubAccountsResponse
from .types.accounts import UpdateAccountRequest
from .types.accountservices import AccountAggregation
from .types.accountservices import AccountManagement
from .types.accountservices import AccountService
from .types.accountservices import ApproveAccountServiceRequest
from .types.accountservices import CampaignsManagement
from .types.accountservices import GetAccountServiceRequest
from .types.accountservices import Handshake
from .types.accountservices import ListAccountServicesRequest
from .types.accountservices import ListAccountServicesResponse
from .types.accountservices import LocalListingManagement
from .types.accountservices import ProductsManagement
from .types.accountservices import ProposeAccountServiceRequest
from .types.accountservices import RejectAccountServiceRequest
from .types.autofeedsettings import AutofeedSettings
from .types.autofeedsettings import GetAutofeedSettingsRequest
from .types.autofeedsettings import UpdateAutofeedSettingsRequest
from .types.automaticimprovements import AutomaticImageImprovements
from .types.automaticimprovements import AutomaticImprovements
from .types.automaticimprovements import AutomaticItemUpdates
from .types.automaticimprovements import AutomaticShippingImprovements
from .types.automaticimprovements import GetAutomaticImprovementsRequest
from .types.automaticimprovements import UpdateAutomaticImprovementsRequest
from .types.businessidentity import BusinessIdentity
from .types.businessidentity import GetBusinessIdentityRequest
from .types.businessidentity import UpdateBusinessIdentityRequest
from .types.businessinfo import BusinessInfo
from .types.businessinfo import GetBusinessInfoRequest
from .types.businessinfo import UpdateBusinessInfoRequest
from .types.checkoutsettings import CheckoutSettings
from .types.checkoutsettings import CreateCheckoutSettingsRequest
from .types.checkoutsettings import DeleteCheckoutSettingsRequest
from .types.checkoutsettings import GetCheckoutSettingsRequest
from .types.checkoutsettings import UpdateCheckoutSettingsRequest
from .types.checkoutsettings import UriSettings
from .types.customerservice import CustomerService
from .types.developerregistration import DeveloperRegistration
from .types.developerregistration import GetDeveloperRegistrationRequest
from .types.developerregistration import RegisterGcpRequest
from .types.developerregistration import UnregisterGcpRequest
from .types.emailpreferences import EmailPreferences
from .types.emailpreferences import GetEmailPreferencesRequest
from .types.emailpreferences import UpdateEmailPreferencesRequest
from .types.gbpaccounts import GbpAccount
from .types.gbpaccounts import LinkGbpAccountRequest
from .types.gbpaccounts import LinkGbpAccountResponse
from .types.gbpaccounts import ListGbpAccountsRequest
from .types.gbpaccounts import ListGbpAccountsResponse
from .types.homepage import ClaimHomepageRequest
from .types.homepage import GetHomepageRequest
from .types.homepage import Homepage
from .types.homepage import UnclaimHomepageRequest
from .types.homepage import UpdateHomepageRequest
from .types.lfpproviders import FindLfpProvidersRequest
from .types.lfpproviders import FindLfpProvidersResponse
from .types.lfpproviders import LfpProvider
from .types.lfpproviders import LinkLfpProviderRequest
from .types.lfpproviders import LinkLfpProviderResponse
from .types.omnichannelsettings import About
from .types.omnichannelsettings import CreateOmnichannelSettingRequest
from .types.omnichannelsettings import GetOmnichannelSettingRequest
from .types.omnichannelsettings import InStock
from .types.omnichannelsettings import InventoryVerification
from .types.omnichannelsettings import LfpLink
from .types.omnichannelsettings import ListOmnichannelSettingsRequest
from .types.omnichannelsettings import ListOmnichannelSettingsResponse
from .types.omnichannelsettings import OmnichannelSetting
from .types.omnichannelsettings import OnDisplayToOrder
from .types.omnichannelsettings import Pickup
from .types.omnichannelsettings import RequestInventoryVerificationRequest
from .types.omnichannelsettings import RequestInventoryVerificationResponse
from .types.omnichannelsettings import ReviewState
from .types.omnichannelsettings import UpdateOmnichannelSettingRequest
from .types.online_return_policy import CreateOnlineReturnPolicyRequest
from .types.online_return_policy import DeleteOnlineReturnPolicyRequest
from .types.online_return_policy import GetOnlineReturnPolicyRequest
from .types.online_return_policy import ListOnlineReturnPoliciesRequest
from .types.online_return_policy import ListOnlineReturnPoliciesResponse
from .types.online_return_policy import OnlineReturnPolicy
from .types.phoneverificationstate import PhoneVerificationState
from .types.programs import DisableProgramRequest
from .types.programs import EnableProgramRequest
from .types.programs import GetProgramRequest
from .types.programs import ListProgramsRequest
from .types.programs import ListProgramsResponse
from .types.programs import Program
from .types.regions import CreateRegionRequest
from .types.regions import DeleteRegionRequest
from .types.regions import GetRegionRequest
from .types.regions import ListRegionsRequest
from .types.regions import ListRegionsResponse
from .types.regions import Region
from .types.regions import UpdateRegionRequest
from .types.shippingsettings import Address
from .types.shippingsettings import BusinessDayConfig
from .types.shippingsettings import CarrierRate
from .types.shippingsettings import CutoffTime
from .types.shippingsettings import DeliveryTime
from .types.shippingsettings import Distance
from .types.shippingsettings import GetShippingSettingsRequest
from .types.shippingsettings import Headers
from .types.shippingsettings import InsertShippingSettingsRequest
from .types.shippingsettings import LocationIdSet
from .types.shippingsettings import MinimumOrderValueTable
from .types.shippingsettings import RateGroup
from .types.shippingsettings import Row
from .types.shippingsettings import Service
from .types.shippingsettings import ShippingSettings
from .types.shippingsettings import Table
from .types.shippingsettings import TransitTable
from .types.shippingsettings import Value
from .types.shippingsettings import Warehouse
from .types.shippingsettings import WarehouseBasedDeliveryTime
from .types.shippingsettings import WarehouseCutoffTime
from .types.termsofservice import AcceptTermsOfServiceRequest
from .types.termsofservice import AcceptTermsOfServiceResponse
from .types.termsofservice import GetTermsOfServiceRequest
from .types.termsofservice import RetrieveLatestTermsOfServiceRequest
from .types.termsofservice import TermsOfService
from .types.termsofserviceagreementstate import Accepted
from .types.termsofserviceagreementstate import GetTermsOfServiceAgreementStateRequest
from .types.termsofserviceagreementstate import Required
from .types.termsofserviceagreementstate import RetrieveForApplicationTermsOfServiceAgreementStateRequest
from .types.termsofserviceagreementstate import TermsOfServiceAgreementState
from .types.termsofservicekind import TermsOfServiceKind
from .types.user import CreateUserRequest
from .types.user import DeleteUserRequest
from .types.user import GetUserRequest
from .types.user import ListUsersRequest
from .types.user import ListUsersResponse
from .types.user import UpdateUserRequest
from .types.user import User

__all__ = (
    'AccountIssueServiceAsyncClient',
    'AccountRelationshipsServiceAsyncClient',
    'AccountServicesServiceAsyncClient',
    'AccountsServiceAsyncClient',
    'AutofeedSettingsServiceAsyncClient',
    'AutomaticImprovementsServiceAsyncClient',
    'BusinessIdentityServiceAsyncClient',
    'BusinessInfoServiceAsyncClient',
    'CheckoutSettingsServiceAsyncClient',
    'DeveloperRegistrationServiceAsyncClient',
    'EmailPreferencesServiceAsyncClient',
    'GbpAccountsServiceAsyncClient',
    'HomepageServiceAsyncClient',
    'LfpProvidersServiceAsyncClient',
    'OmnichannelSettingsServiceAsyncClient',
    'OnlineReturnPolicyServiceAsyncClient',
    'ProgramsServiceAsyncClient',
    'RegionsServiceAsyncClient',
    'ShippingSettingsServiceAsyncClient',
    'TermsOfServiceAgreementStateServiceAsyncClient',
    'TermsOfServiceServiceAsyncClient',
    'UserServiceAsyncClient',
'About',
'AcceptTermsOfServiceRequest',
'AcceptTermsOfServiceResponse',
'Accepted',
'AccessRight',
'Account',
'AccountAggregation',
'AccountIssue',
'AccountIssueServiceClient',
'AccountManagement',
'AccountRelationship',
'AccountRelationshipsServiceClient',
'AccountService',
'AccountServicesServiceClient',
'AccountsServiceClient',
'Address',
'ApproveAccountServiceRequest',
'AutofeedSettings',
'AutofeedSettingsServiceClient',
'AutomaticImageImprovements',
'AutomaticImprovements',
'AutomaticImprovementsServiceClient',
'AutomaticItemUpdates',
'AutomaticShippingImprovements',
'BusinessDayConfig',
'BusinessIdentity',
'BusinessIdentityServiceClient',
'BusinessInfo',
'BusinessInfoServiceClient',
'CampaignsManagement',
'CarrierRate',
'CheckoutSettings',
'CheckoutSettingsServiceClient',
'ClaimHomepageRequest',
'CreateAndConfigureAccountRequest',
'CreateCheckoutSettingsRequest',
'CreateOmnichannelSettingRequest',
'CreateOnlineReturnPolicyRequest',
'CreateRegionRequest',
'CreateUserRequest',
'CustomerService',
'CutoffTime',
'DeleteAccountRequest',
'DeleteCheckoutSettingsRequest',
'DeleteOnlineReturnPolicyRequest',
'DeleteRegionRequest',
'DeleteUserRequest',
'DeliveryTime',
'DeveloperRegistration',
'DeveloperRegistrationServiceClient',
'DisableProgramRequest',
'Distance',
'EmailPreferences',
'EmailPreferencesServiceClient',
'EnableProgramRequest',
'FindLfpProvidersRequest',
'FindLfpProvidersResponse',
'GbpAccount',
'GbpAccountsServiceClient',
'GetAccountRelationshipRequest',
'GetAccountRequest',
'GetAccountServiceRequest',
'GetAutofeedSettingsRequest',
'GetAutomaticImprovementsRequest',
'GetBusinessIdentityRequest',
'GetBusinessInfoRequest',
'GetCheckoutSettingsRequest',
'GetDeveloperRegistrationRequest',
'GetEmailPreferencesRequest',
'GetHomepageRequest',
'GetOmnichannelSettingRequest',
'GetOnlineReturnPolicyRequest',
'GetProgramRequest',
'GetRegionRequest',
'GetShippingSettingsRequest',
'GetTermsOfServiceAgreementStateRequest',
'GetTermsOfServiceRequest',
'GetUserRequest',
'Handshake',
'Headers',
'Homepage',
'HomepageServiceClient',
'InStock',
'InsertShippingSettingsRequest',
'InventoryVerification',
'LfpLink',
'LfpProvider',
'LfpProvidersServiceClient',
'LinkGbpAccountRequest',
'LinkGbpAccountResponse',
'LinkLfpProviderRequest',
'LinkLfpProviderResponse',
'ListAccountIssuesRequest',
'ListAccountIssuesResponse',
'ListAccountRelationshipsRequest',
'ListAccountRelationshipsResponse',
'ListAccountServicesRequest',
'ListAccountServicesResponse',
'ListAccountsRequest',
'ListAccountsResponse',
'ListGbpAccountsRequest',
'ListGbpAccountsResponse',
'ListOmnichannelSettingsRequest',
'ListOmnichannelSettingsResponse',
'ListOnlineReturnPoliciesRequest',
'ListOnlineReturnPoliciesResponse',
'ListProgramsRequest',
'ListProgramsResponse',
'ListRegionsRequest',
'ListRegionsResponse',
'ListSubAccountsRequest',
'ListSubAccountsResponse',
'ListUsersRequest',
'ListUsersResponse',
'LocalListingManagement',
'LocationIdSet',
'MinimumOrderValueTable',
'OmnichannelSetting',
'OmnichannelSettingsServiceClient',
'OnDisplayToOrder',
'OnlineReturnPolicy',
'OnlineReturnPolicyServiceClient',
'PhoneVerificationState',
'Pickup',
'ProductsManagement',
'Program',
'ProgramsServiceClient',
'ProposeAccountServiceRequest',
'RateGroup',
'Region',
'RegionsServiceClient',
'RegisterGcpRequest',
'RejectAccountServiceRequest',
'RequestInventoryVerificationRequest',
'RequestInventoryVerificationResponse',
'Required',
'RetrieveForApplicationTermsOfServiceAgreementStateRequest',
'RetrieveLatestTermsOfServiceRequest',
'ReviewState',
'Row',
'Service',
'ShippingSettings',
'ShippingSettingsServiceClient',
'Table',
'TermsOfService',
'TermsOfServiceAgreementState',
'TermsOfServiceAgreementStateServiceClient',
'TermsOfServiceKind',
'TermsOfServiceServiceClient',
'TransitTable',
'UnclaimHomepageRequest',
'UnregisterGcpRequest',
'UpdateAccountRelationshipRequest',
'UpdateAccountRequest',
'UpdateAutofeedSettingsRequest',
'UpdateAutomaticImprovementsRequest',
'UpdateBusinessIdentityRequest',
'UpdateBusinessInfoRequest',
'UpdateCheckoutSettingsRequest',
'UpdateEmailPreferencesRequest',
'UpdateHomepageRequest',
'UpdateOmnichannelSettingRequest',
'UpdateRegionRequest',
'UpdateUserRequest',
'UriSettings',
'User',
'UserServiceClient',
'Value',
'Warehouse',
'WarehouseBasedDeliveryTime',
'WarehouseCutoffTime',
)
