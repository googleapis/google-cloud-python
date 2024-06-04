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
from google.shopping.merchant_accounts_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.account_issue_service import (
    AccountIssueServiceAsyncClient,
    AccountIssueServiceClient,
)
from .services.account_tax_service import (
    AccountTaxServiceAsyncClient,
    AccountTaxServiceClient,
)
from .services.accounts_service import AccountsServiceAsyncClient, AccountsServiceClient
from .services.business_identity_service import (
    BusinessIdentityServiceAsyncClient,
    BusinessIdentityServiceClient,
)
from .services.business_info_service import (
    BusinessInfoServiceAsyncClient,
    BusinessInfoServiceClient,
)
from .services.email_preferences_service import (
    EmailPreferencesServiceAsyncClient,
    EmailPreferencesServiceClient,
)
from .services.homepage_service import HomepageServiceAsyncClient, HomepageServiceClient
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
from .types.account_tax import (
    AccountTax,
    GetAccountTaxRequest,
    ListAccountTaxRequest,
    ListAccountTaxResponse,
    UpdateAccountTaxRequest,
)
from .types.accountissue import (
    AccountIssue,
    ListAccountIssuesRequest,
    ListAccountIssuesResponse,
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
from .types.customerservice import CustomerService
from .types.emailpreferences import (
    EmailPreferences,
    GetEmailPreferencesRequest,
    UpdateEmailPreferencesRequest,
)
from .types.homepage import (
    ClaimHomepageRequest,
    GetHomepageRequest,
    Homepage,
    UnclaimHomepageRequest,
    UpdateHomepageRequest,
)
from .types.online_return_policy import (
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
from .types.tax_rule import TaxRule
from .types.termsofservice import (
    AcceptTermsOfServiceRequest,
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
    "AccountTaxServiceAsyncClient",
    "AccountsServiceAsyncClient",
    "BusinessIdentityServiceAsyncClient",
    "BusinessInfoServiceAsyncClient",
    "EmailPreferencesServiceAsyncClient",
    "HomepageServiceAsyncClient",
    "OnlineReturnPolicyServiceAsyncClient",
    "ProgramsServiceAsyncClient",
    "RegionsServiceAsyncClient",
    "ShippingSettingsServiceAsyncClient",
    "TermsOfServiceAgreementStateServiceAsyncClient",
    "TermsOfServiceServiceAsyncClient",
    "UserServiceAsyncClient",
    "AcceptTermsOfServiceRequest",
    "Accepted",
    "AccessRight",
    "Account",
    "AccountIssue",
    "AccountIssueServiceClient",
    "AccountTax",
    "AccountTaxServiceClient",
    "AccountsServiceClient",
    "Address",
    "BusinessDayConfig",
    "BusinessIdentity",
    "BusinessIdentityServiceClient",
    "BusinessInfo",
    "BusinessInfoServiceClient",
    "CarrierRate",
    "ClaimHomepageRequest",
    "CreateAndConfigureAccountRequest",
    "CreateRegionRequest",
    "CreateUserRequest",
    "CustomerService",
    "CutoffTime",
    "DeleteAccountRequest",
    "DeleteRegionRequest",
    "DeleteUserRequest",
    "DeliveryTime",
    "DisableProgramRequest",
    "Distance",
    "EmailPreferences",
    "EmailPreferencesServiceClient",
    "EnableProgramRequest",
    "GetAccountRequest",
    "GetAccountTaxRequest",
    "GetBusinessIdentityRequest",
    "GetBusinessInfoRequest",
    "GetEmailPreferencesRequest",
    "GetHomepageRequest",
    "GetOnlineReturnPolicyRequest",
    "GetProgramRequest",
    "GetRegionRequest",
    "GetShippingSettingsRequest",
    "GetTermsOfServiceAgreementStateRequest",
    "GetTermsOfServiceRequest",
    "GetUserRequest",
    "Headers",
    "Homepage",
    "HomepageServiceClient",
    "InsertShippingSettingsRequest",
    "ListAccountIssuesRequest",
    "ListAccountIssuesResponse",
    "ListAccountTaxRequest",
    "ListAccountTaxResponse",
    "ListAccountsRequest",
    "ListAccountsResponse",
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
    "LocationIdSet",
    "MinimumOrderValueTable",
    "OnlineReturnPolicy",
    "OnlineReturnPolicyServiceClient",
    "PhoneVerificationState",
    "Program",
    "ProgramsServiceClient",
    "RateGroup",
    "Region",
    "RegionsServiceClient",
    "Required",
    "RetrieveForApplicationTermsOfServiceAgreementStateRequest",
    "RetrieveLatestTermsOfServiceRequest",
    "Row",
    "Service",
    "ShippingSettings",
    "ShippingSettingsServiceClient",
    "Table",
    "TaxRule",
    "TermsOfService",
    "TermsOfServiceAgreementState",
    "TermsOfServiceAgreementStateServiceClient",
    "TermsOfServiceKind",
    "TermsOfServiceServiceClient",
    "TransitTable",
    "UnclaimHomepageRequest",
    "UpdateAccountRequest",
    "UpdateAccountTaxRequest",
    "UpdateBusinessIdentityRequest",
    "UpdateBusinessInfoRequest",
    "UpdateEmailPreferencesRequest",
    "UpdateHomepageRequest",
    "UpdateRegionRequest",
    "UpdateUserRequest",
    "User",
    "UserServiceClient",
    "Value",
    "Warehouse",
    "WarehouseBasedDeliveryTime",
    "WarehouseCutoffTime",
)
