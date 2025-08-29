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


from .services.account_issue_service import (
    AccountIssueServiceAsyncClient,
    AccountIssueServiceClient,
)
from .services.account_relationships_service import (
    AccountRelationshipsServiceAsyncClient,
    AccountRelationshipsServiceClient,
)
from .services.account_services_service import (
    AccountServicesServiceAsyncClient,
    AccountServicesServiceClient,
)
from .services.accounts_service import AccountsServiceAsyncClient, AccountsServiceClient
from .services.autofeed_settings_service import (
    AutofeedSettingsServiceAsyncClient,
    AutofeedSettingsServiceClient,
)
from .services.automatic_improvements_service import (
    AutomaticImprovementsServiceAsyncClient,
    AutomaticImprovementsServiceClient,
)
from .services.business_identity_service import (
    BusinessIdentityServiceAsyncClient,
    BusinessIdentityServiceClient,
)
from .services.business_info_service import (
    BusinessInfoServiceAsyncClient,
    BusinessInfoServiceClient,
)
from .services.checkout_settings_service import (
    CheckoutSettingsServiceAsyncClient,
    CheckoutSettingsServiceClient,
)
from .services.developer_registration_service import (
    DeveloperRegistrationServiceAsyncClient,
    DeveloperRegistrationServiceClient,
)
from .services.email_preferences_service import (
    EmailPreferencesServiceAsyncClient,
    EmailPreferencesServiceClient,
)
from .services.gbp_accounts_service import (
    GbpAccountsServiceAsyncClient,
    GbpAccountsServiceClient,
)
from .services.homepage_service import HomepageServiceAsyncClient, HomepageServiceClient
from .services.lfp_providers_service import (
    LfpProvidersServiceAsyncClient,
    LfpProvidersServiceClient,
)
from .services.omnichannel_settings_service import (
    OmnichannelSettingsServiceAsyncClient,
    OmnichannelSettingsServiceClient,
)
from .services.online_return_policy_service import (
    OnlineReturnPolicyServiceAsyncClient,
    OnlineReturnPolicyServiceClient,
)
from .services.programs_service import ProgramsServiceAsyncClient, ProgramsServiceClient
from .services.regions_service import RegionsServiceAsyncClient, RegionsServiceClient
from .services.shipping_settings_service import (
    ShippingSettingsServiceAsyncClient,
    ShippingSettingsServiceClient,
)
from .services.terms_of_service_agreement_state_service import (
    TermsOfServiceAgreementStateServiceAsyncClient,
    TermsOfServiceAgreementStateServiceClient,
)
from .services.terms_of_service_service import (
    TermsOfServiceServiceAsyncClient,
    TermsOfServiceServiceClient,
)
from .services.user_service import UserServiceAsyncClient, UserServiceClient
from .types.accessright import AccessRight
from .types.accountissue import (
    AccountIssue,
    ListAccountIssuesRequest,
    ListAccountIssuesResponse,
)
from .types.accountrelationships import (
    AccountRelationship,
    GetAccountRelationshipRequest,
    ListAccountRelationshipsRequest,
    ListAccountRelationshipsResponse,
    UpdateAccountRelationshipRequest,
)
from .types.accounts import (
    Account,
    CreateAndConfigureAccountRequest,
    DeleteAccountRequest,
    GetAccountRequest,
    ListAccountsRequest,
    ListAccountsResponse,
    ListSubAccountsRequest,
    ListSubAccountsResponse,
    UpdateAccountRequest,
)
from .types.accountservices import (
    AccountAggregation,
    AccountManagement,
    AccountService,
    ApproveAccountServiceRequest,
    CampaignsManagement,
    GetAccountServiceRequest,
    Handshake,
    ListAccountServicesRequest,
    ListAccountServicesResponse,
    LocalListingManagement,
    ProductsManagement,
    ProposeAccountServiceRequest,
    RejectAccountServiceRequest,
)
from .types.autofeedsettings import (
    AutofeedSettings,
    GetAutofeedSettingsRequest,
    UpdateAutofeedSettingsRequest,
)
from .types.automaticimprovements import (
    AutomaticImageImprovements,
    AutomaticImprovements,
    AutomaticItemUpdates,
    AutomaticShippingImprovements,
    GetAutomaticImprovementsRequest,
    UpdateAutomaticImprovementsRequest,
)
from .types.businessidentity import (
    BusinessIdentity,
    GetBusinessIdentityRequest,
    UpdateBusinessIdentityRequest,
)
from .types.businessinfo import (
    BusinessInfo,
    GetBusinessInfoRequest,
    UpdateBusinessInfoRequest,
)
from .types.checkoutsettings import (
    CheckoutSettings,
    CreateCheckoutSettingsRequest,
    DeleteCheckoutSettingsRequest,
    GetCheckoutSettingsRequest,
    UpdateCheckoutSettingsRequest,
    UriSettings,
)
from .types.customerservice import CustomerService
from .types.developerregistration import (
    DeveloperRegistration,
    GetDeveloperRegistrationRequest,
    RegisterGcpRequest,
    UnregisterGcpRequest,
)
from .types.emailpreferences import (
    EmailPreferences,
    GetEmailPreferencesRequest,
    UpdateEmailPreferencesRequest,
)
from .types.gbpaccounts import (
    GbpAccount,
    LinkGbpAccountRequest,
    LinkGbpAccountResponse,
    ListGbpAccountsRequest,
    ListGbpAccountsResponse,
)
from .types.homepage import (
    ClaimHomepageRequest,
    GetHomepageRequest,
    Homepage,
    UnclaimHomepageRequest,
    UpdateHomepageRequest,
)
from .types.lfpproviders import (
    FindLfpProvidersRequest,
    FindLfpProvidersResponse,
    LfpProvider,
    LinkLfpProviderRequest,
    LinkLfpProviderResponse,
)
from .types.omnichannelsettings import (
    About,
    CreateOmnichannelSettingRequest,
    GetOmnichannelSettingRequest,
    InStock,
    InventoryVerification,
    LfpLink,
    ListOmnichannelSettingsRequest,
    ListOmnichannelSettingsResponse,
    OmnichannelSetting,
    OnDisplayToOrder,
    Pickup,
    RequestInventoryVerificationRequest,
    RequestInventoryVerificationResponse,
    ReviewState,
    UpdateOmnichannelSettingRequest,
)
from .types.online_return_policy import (
    CreateOnlineReturnPolicyRequest,
    DeleteOnlineReturnPolicyRequest,
    GetOnlineReturnPolicyRequest,
    ListOnlineReturnPoliciesRequest,
    ListOnlineReturnPoliciesResponse,
    OnlineReturnPolicy,
)
from .types.phoneverificationstate import PhoneVerificationState
from .types.programs import (
    DisableProgramRequest,
    EnableProgramRequest,
    GetProgramRequest,
    ListProgramsRequest,
    ListProgramsResponse,
    Program,
)
from .types.regions import (
    BatchCreateRegionsRequest,
    BatchCreateRegionsResponse,
    BatchDeleteRegionsRequest,
    BatchUpdateRegionsRequest,
    BatchUpdateRegionsResponse,
    CreateRegionRequest,
    DeleteRegionRequest,
    GetRegionRequest,
    ListRegionsRequest,
    ListRegionsResponse,
    Region,
    UpdateRegionRequest,
)
from .types.shippingsettings import (
    Address,
    BusinessDayConfig,
    CarrierRate,
    CutoffTime,
    DeliveryTime,
    Distance,
    GetShippingSettingsRequest,
    Headers,
    InsertShippingSettingsRequest,
    LocationIdSet,
    MinimumOrderValueTable,
    RateGroup,
    Row,
    Service,
    ShippingSettings,
    Table,
    TransitTable,
    Value,
    Warehouse,
    WarehouseBasedDeliveryTime,
    WarehouseCutoffTime,
)
from .types.termsofservice import (
    AcceptTermsOfServiceRequest,
    AcceptTermsOfServiceResponse,
    GetTermsOfServiceRequest,
    RetrieveLatestTermsOfServiceRequest,
    TermsOfService,
)
from .types.termsofserviceagreementstate import (
    Accepted,
    GetTermsOfServiceAgreementStateRequest,
    Required,
    RetrieveForApplicationTermsOfServiceAgreementStateRequest,
    TermsOfServiceAgreementState,
)
from .types.termsofservicekind import TermsOfServiceKind
from .types.user import (
    CreateUserRequest,
    DeleteUserRequest,
    GetUserRequest,
    ListUsersRequest,
    ListUsersResponse,
    UpdateUserRequest,
    User,
)

__all__ = (
    "AccountIssueServiceAsyncClient",
    "AccountRelationshipsServiceAsyncClient",
    "AccountServicesServiceAsyncClient",
    "AccountsServiceAsyncClient",
    "AutofeedSettingsServiceAsyncClient",
    "AutomaticImprovementsServiceAsyncClient",
    "BusinessIdentityServiceAsyncClient",
    "BusinessInfoServiceAsyncClient",
    "CheckoutSettingsServiceAsyncClient",
    "DeveloperRegistrationServiceAsyncClient",
    "EmailPreferencesServiceAsyncClient",
    "GbpAccountsServiceAsyncClient",
    "HomepageServiceAsyncClient",
    "LfpProvidersServiceAsyncClient",
    "OmnichannelSettingsServiceAsyncClient",
    "OnlineReturnPolicyServiceAsyncClient",
    "ProgramsServiceAsyncClient",
    "RegionsServiceAsyncClient",
    "ShippingSettingsServiceAsyncClient",
    "TermsOfServiceAgreementStateServiceAsyncClient",
    "TermsOfServiceServiceAsyncClient",
    "UserServiceAsyncClient",
    "About",
    "AcceptTermsOfServiceRequest",
    "AcceptTermsOfServiceResponse",
    "Accepted",
    "AccessRight",
    "Account",
    "AccountAggregation",
    "AccountIssue",
    "AccountIssueServiceClient",
    "AccountManagement",
    "AccountRelationship",
    "AccountRelationshipsServiceClient",
    "AccountService",
    "AccountServicesServiceClient",
    "AccountsServiceClient",
    "Address",
    "ApproveAccountServiceRequest",
    "AutofeedSettings",
    "AutofeedSettingsServiceClient",
    "AutomaticImageImprovements",
    "AutomaticImprovements",
    "AutomaticImprovementsServiceClient",
    "AutomaticItemUpdates",
    "AutomaticShippingImprovements",
    "BatchCreateRegionsRequest",
    "BatchCreateRegionsResponse",
    "BatchDeleteRegionsRequest",
    "BatchUpdateRegionsRequest",
    "BatchUpdateRegionsResponse",
    "BusinessDayConfig",
    "BusinessIdentity",
    "BusinessIdentityServiceClient",
    "BusinessInfo",
    "BusinessInfoServiceClient",
    "CampaignsManagement",
    "CarrierRate",
    "CheckoutSettings",
    "CheckoutSettingsServiceClient",
    "ClaimHomepageRequest",
    "CreateAndConfigureAccountRequest",
    "CreateCheckoutSettingsRequest",
    "CreateOmnichannelSettingRequest",
    "CreateOnlineReturnPolicyRequest",
    "CreateRegionRequest",
    "CreateUserRequest",
    "CustomerService",
    "CutoffTime",
    "DeleteAccountRequest",
    "DeleteCheckoutSettingsRequest",
    "DeleteOnlineReturnPolicyRequest",
    "DeleteRegionRequest",
    "DeleteUserRequest",
    "DeliveryTime",
    "DeveloperRegistration",
    "DeveloperRegistrationServiceClient",
    "DisableProgramRequest",
    "Distance",
    "EmailPreferences",
    "EmailPreferencesServiceClient",
    "EnableProgramRequest",
    "FindLfpProvidersRequest",
    "FindLfpProvidersResponse",
    "GbpAccount",
    "GbpAccountsServiceClient",
    "GetAccountRelationshipRequest",
    "GetAccountRequest",
    "GetAccountServiceRequest",
    "GetAutofeedSettingsRequest",
    "GetAutomaticImprovementsRequest",
    "GetBusinessIdentityRequest",
    "GetBusinessInfoRequest",
    "GetCheckoutSettingsRequest",
    "GetDeveloperRegistrationRequest",
    "GetEmailPreferencesRequest",
    "GetHomepageRequest",
    "GetOmnichannelSettingRequest",
    "GetOnlineReturnPolicyRequest",
    "GetProgramRequest",
    "GetRegionRequest",
    "GetShippingSettingsRequest",
    "GetTermsOfServiceAgreementStateRequest",
    "GetTermsOfServiceRequest",
    "GetUserRequest",
    "Handshake",
    "Headers",
    "Homepage",
    "HomepageServiceClient",
    "InStock",
    "InsertShippingSettingsRequest",
    "InventoryVerification",
    "LfpLink",
    "LfpProvider",
    "LfpProvidersServiceClient",
    "LinkGbpAccountRequest",
    "LinkGbpAccountResponse",
    "LinkLfpProviderRequest",
    "LinkLfpProviderResponse",
    "ListAccountIssuesRequest",
    "ListAccountIssuesResponse",
    "ListAccountRelationshipsRequest",
    "ListAccountRelationshipsResponse",
    "ListAccountServicesRequest",
    "ListAccountServicesResponse",
    "ListAccountsRequest",
    "ListAccountsResponse",
    "ListGbpAccountsRequest",
    "ListGbpAccountsResponse",
    "ListOmnichannelSettingsRequest",
    "ListOmnichannelSettingsResponse",
    "ListOnlineReturnPoliciesRequest",
    "ListOnlineReturnPoliciesResponse",
    "ListProgramsRequest",
    "ListProgramsResponse",
    "ListRegionsRequest",
    "ListRegionsResponse",
    "ListSubAccountsRequest",
    "ListSubAccountsResponse",
    "ListUsersRequest",
    "ListUsersResponse",
    "LocalListingManagement",
    "LocationIdSet",
    "MinimumOrderValueTable",
    "OmnichannelSetting",
    "OmnichannelSettingsServiceClient",
    "OnDisplayToOrder",
    "OnlineReturnPolicy",
    "OnlineReturnPolicyServiceClient",
    "PhoneVerificationState",
    "Pickup",
    "ProductsManagement",
    "Program",
    "ProgramsServiceClient",
    "ProposeAccountServiceRequest",
    "RateGroup",
    "Region",
    "RegionsServiceClient",
    "RegisterGcpRequest",
    "RejectAccountServiceRequest",
    "RequestInventoryVerificationRequest",
    "RequestInventoryVerificationResponse",
    "Required",
    "RetrieveForApplicationTermsOfServiceAgreementStateRequest",
    "RetrieveLatestTermsOfServiceRequest",
    "ReviewState",
    "Row",
    "Service",
    "ShippingSettings",
    "ShippingSettingsServiceClient",
    "Table",
    "TermsOfService",
    "TermsOfServiceAgreementState",
    "TermsOfServiceAgreementStateServiceClient",
    "TermsOfServiceKind",
    "TermsOfServiceServiceClient",
    "TransitTable",
    "UnclaimHomepageRequest",
    "UnregisterGcpRequest",
    "UpdateAccountRelationshipRequest",
    "UpdateAccountRequest",
    "UpdateAutofeedSettingsRequest",
    "UpdateAutomaticImprovementsRequest",
    "UpdateBusinessIdentityRequest",
    "UpdateBusinessInfoRequest",
    "UpdateCheckoutSettingsRequest",
    "UpdateEmailPreferencesRequest",
    "UpdateHomepageRequest",
    "UpdateOmnichannelSettingRequest",
    "UpdateRegionRequest",
    "UpdateUserRequest",
    "UriSettings",
    "User",
    "UserServiceClient",
    "Value",
    "Warehouse",
    "WarehouseBasedDeliveryTime",
    "WarehouseCutoffTime",
)
