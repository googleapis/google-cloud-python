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
from google.shopping.merchant_accounts import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_accounts_v1beta.services.account_issue_service.async_client import (
    AccountIssueServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.account_issue_service.client import (
    AccountIssueServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.account_tax_service.async_client import (
    AccountTaxServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.account_tax_service.client import (
    AccountTaxServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.accounts_service.async_client import (
    AccountsServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.accounts_service.client import (
    AccountsServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.business_identity_service.async_client import (
    BusinessIdentityServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.business_identity_service.client import (
    BusinessIdentityServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.business_info_service.async_client import (
    BusinessInfoServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.business_info_service.client import (
    BusinessInfoServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.email_preferences_service.async_client import (
    EmailPreferencesServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.email_preferences_service.client import (
    EmailPreferencesServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.homepage_service.async_client import (
    HomepageServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.homepage_service.client import (
    HomepageServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.online_return_policy_service.async_client import (
    OnlineReturnPolicyServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.online_return_policy_service.client import (
    OnlineReturnPolicyServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.programs_service.async_client import (
    ProgramsServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.programs_service.client import (
    ProgramsServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.regions_service.async_client import (
    RegionsServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.regions_service.client import (
    RegionsServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.shipping_settings_service.async_client import (
    ShippingSettingsServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.shipping_settings_service.client import (
    ShippingSettingsServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.terms_of_service_agreement_state_service.async_client import (
    TermsOfServiceAgreementStateServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.terms_of_service_agreement_state_service.client import (
    TermsOfServiceAgreementStateServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.terms_of_service_service.async_client import (
    TermsOfServiceServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.terms_of_service_service.client import (
    TermsOfServiceServiceClient,
)
from google.shopping.merchant_accounts_v1beta.services.user_service.async_client import (
    UserServiceAsyncClient,
)
from google.shopping.merchant_accounts_v1beta.services.user_service.client import (
    UserServiceClient,
)
from google.shopping.merchant_accounts_v1beta.types.accessright import AccessRight
from google.shopping.merchant_accounts_v1beta.types.account_tax import (
    AccountTax,
    GetAccountTaxRequest,
    ListAccountTaxRequest,
    ListAccountTaxResponse,
    UpdateAccountTaxRequest,
)
from google.shopping.merchant_accounts_v1beta.types.accountissue import (
    AccountIssue,
    ListAccountIssuesRequest,
    ListAccountIssuesResponse,
)
from google.shopping.merchant_accounts_v1beta.types.accounts import (
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
from google.shopping.merchant_accounts_v1beta.types.businessidentity import (
    BusinessIdentity,
    GetBusinessIdentityRequest,
    UpdateBusinessIdentityRequest,
)
from google.shopping.merchant_accounts_v1beta.types.businessinfo import (
    BusinessInfo,
    GetBusinessInfoRequest,
    UpdateBusinessInfoRequest,
)
from google.shopping.merchant_accounts_v1beta.types.customerservice import (
    CustomerService,
)
from google.shopping.merchant_accounts_v1beta.types.emailpreferences import (
    EmailPreferences,
    GetEmailPreferencesRequest,
    UpdateEmailPreferencesRequest,
)
from google.shopping.merchant_accounts_v1beta.types.homepage import (
    ClaimHomepageRequest,
    GetHomepageRequest,
    Homepage,
    UnclaimHomepageRequest,
    UpdateHomepageRequest,
)
from google.shopping.merchant_accounts_v1beta.types.online_return_policy import (
    GetOnlineReturnPolicyRequest,
    ListOnlineReturnPoliciesRequest,
    ListOnlineReturnPoliciesResponse,
    OnlineReturnPolicy,
)
from google.shopping.merchant_accounts_v1beta.types.phoneverificationstate import (
    PhoneVerificationState,
)
from google.shopping.merchant_accounts_v1beta.types.programs import (
    DisableProgramRequest,
    EnableProgramRequest,
    GetProgramRequest,
    ListProgramsRequest,
    ListProgramsResponse,
    Program,
)
from google.shopping.merchant_accounts_v1beta.types.regions import (
    CreateRegionRequest,
    DeleteRegionRequest,
    GetRegionRequest,
    ListRegionsRequest,
    ListRegionsResponse,
    Region,
    UpdateRegionRequest,
)
from google.shopping.merchant_accounts_v1beta.types.shippingsettings import (
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
from google.shopping.merchant_accounts_v1beta.types.tax_rule import TaxRule
from google.shopping.merchant_accounts_v1beta.types.termsofservice import (
    AcceptTermsOfServiceRequest,
    GetTermsOfServiceRequest,
    RetrieveLatestTermsOfServiceRequest,
    TermsOfService,
)
from google.shopping.merchant_accounts_v1beta.types.termsofserviceagreementstate import (
    Accepted,
    GetTermsOfServiceAgreementStateRequest,
    Required,
    RetrieveForApplicationTermsOfServiceAgreementStateRequest,
    TermsOfServiceAgreementState,
)
from google.shopping.merchant_accounts_v1beta.types.termsofservicekind import (
    TermsOfServiceKind,
)
from google.shopping.merchant_accounts_v1beta.types.user import (
    CreateUserRequest,
    DeleteUserRequest,
    GetUserRequest,
    ListUsersRequest,
    ListUsersResponse,
    UpdateUserRequest,
    User,
)

__all__ = (
    "AccountIssueServiceClient",
    "AccountIssueServiceAsyncClient",
    "AccountsServiceClient",
    "AccountsServiceAsyncClient",
    "AccountTaxServiceClient",
    "AccountTaxServiceAsyncClient",
    "BusinessIdentityServiceClient",
    "BusinessIdentityServiceAsyncClient",
    "BusinessInfoServiceClient",
    "BusinessInfoServiceAsyncClient",
    "EmailPreferencesServiceClient",
    "EmailPreferencesServiceAsyncClient",
    "HomepageServiceClient",
    "HomepageServiceAsyncClient",
    "OnlineReturnPolicyServiceClient",
    "OnlineReturnPolicyServiceAsyncClient",
    "ProgramsServiceClient",
    "ProgramsServiceAsyncClient",
    "RegionsServiceClient",
    "RegionsServiceAsyncClient",
    "ShippingSettingsServiceClient",
    "ShippingSettingsServiceAsyncClient",
    "TermsOfServiceAgreementStateServiceClient",
    "TermsOfServiceAgreementStateServiceAsyncClient",
    "TermsOfServiceServiceClient",
    "TermsOfServiceServiceAsyncClient",
    "UserServiceClient",
    "UserServiceAsyncClient",
    "AccessRight",
    "AccountTax",
    "GetAccountTaxRequest",
    "ListAccountTaxRequest",
    "ListAccountTaxResponse",
    "UpdateAccountTaxRequest",
    "AccountIssue",
    "ListAccountIssuesRequest",
    "ListAccountIssuesResponse",
    "Account",
    "CreateAndConfigureAccountRequest",
    "DeleteAccountRequest",
    "GetAccountRequest",
    "ListAccountsRequest",
    "ListAccountsResponse",
    "ListSubAccountsRequest",
    "ListSubAccountsResponse",
    "UpdateAccountRequest",
    "BusinessIdentity",
    "GetBusinessIdentityRequest",
    "UpdateBusinessIdentityRequest",
    "BusinessInfo",
    "GetBusinessInfoRequest",
    "UpdateBusinessInfoRequest",
    "CustomerService",
    "EmailPreferences",
    "GetEmailPreferencesRequest",
    "UpdateEmailPreferencesRequest",
    "ClaimHomepageRequest",
    "GetHomepageRequest",
    "Homepage",
    "UnclaimHomepageRequest",
    "UpdateHomepageRequest",
    "GetOnlineReturnPolicyRequest",
    "ListOnlineReturnPoliciesRequest",
    "ListOnlineReturnPoliciesResponse",
    "OnlineReturnPolicy",
    "PhoneVerificationState",
    "DisableProgramRequest",
    "EnableProgramRequest",
    "GetProgramRequest",
    "ListProgramsRequest",
    "ListProgramsResponse",
    "Program",
    "CreateRegionRequest",
    "DeleteRegionRequest",
    "GetRegionRequest",
    "ListRegionsRequest",
    "ListRegionsResponse",
    "Region",
    "UpdateRegionRequest",
    "Address",
    "BusinessDayConfig",
    "CarrierRate",
    "CutoffTime",
    "DeliveryTime",
    "Distance",
    "GetShippingSettingsRequest",
    "Headers",
    "InsertShippingSettingsRequest",
    "LocationIdSet",
    "MinimumOrderValueTable",
    "RateGroup",
    "Row",
    "Service",
    "ShippingSettings",
    "Table",
    "TransitTable",
    "Value",
    "Warehouse",
    "WarehouseBasedDeliveryTime",
    "WarehouseCutoffTime",
    "TaxRule",
    "AcceptTermsOfServiceRequest",
    "GetTermsOfServiceRequest",
    "RetrieveLatestTermsOfServiceRequest",
    "TermsOfService",
    "Accepted",
    "GetTermsOfServiceAgreementStateRequest",
    "Required",
    "RetrieveForApplicationTermsOfServiceAgreementStateRequest",
    "TermsOfServiceAgreementState",
    "TermsOfServiceKind",
    "CreateUserRequest",
    "DeleteUserRequest",
    "GetUserRequest",
    "ListUsersRequest",
    "ListUsersResponse",
    "UpdateUserRequest",
    "User",
)
