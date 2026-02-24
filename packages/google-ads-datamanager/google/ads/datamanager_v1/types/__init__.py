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
from .age_range import (
    AgeRange,
)
from .audience import (
    AudienceMember,
    MobileData,
    PairData,
    PpidData,
    UserIdData,
)
from .cart_data import (
    CartData,
    Item,
)
from .consent import (
    Consent,
    ConsentStatus,
)
from .destination import (
    Destination,
    Product,
    ProductAccount,
)
from .device_info import (
    DeviceInfo,
)
from .encryption_info import (
    AwsWrappedKeyInfo,
    EncryptionInfo,
    GcpWrappedKeyInfo,
)
from .error import (
    ErrorReason,
)
from .event import (
    AdIdentifiers,
    CustomVariable,
    Event,
    EventParameter,
    EventSource,
)
from .experimental_field import (
    ExperimentalField,
)
from .gender import (
    Gender,
)
from .ingestion_service import (
    Encoding,
    IngestAudienceMembersRequest,
    IngestAudienceMembersResponse,
    IngestEventsRequest,
    IngestEventsResponse,
    RemoveAudienceMembersRequest,
    RemoveAudienceMembersResponse,
    RetrieveRequestStatusRequest,
    RetrieveRequestStatusResponse,
)
from .insights_service import (
    Baseline,
    RetrieveInsightsRequest,
    RetrieveInsightsResponse,
)
from .item_parameter import (
    ItemParameter,
)
from .match_rate import (
    MatchRateRange,
)
from .partner_link_service import (
    CreatePartnerLinkRequest,
    DeletePartnerLinkRequest,
    PartnerLink,
    SearchPartnerLinksRequest,
    SearchPartnerLinksResponse,
)
from .processing_errors import (
    ErrorCount,
    ErrorInfo,
    ProcessingErrorReason,
    ProcessingWarningReason,
    WarningCount,
    WarningInfo,
)
from .request_status_per_destination import (
    RequestStatusPerDestination,
)
from .terms_of_service import (
    TermsOfService,
    TermsOfServiceStatus,
)
from .user_data import (
    AddressInfo,
    UserData,
    UserIdentifier,
)
from .user_list import (
    ContactIdInfo,
    DataSourceType,
    IngestedUserListInfo,
    MobileIdInfo,
    PairIdInfo,
    PartnerAudienceInfo,
    PseudonymousIdInfo,
    SizeInfo,
    TargetNetworkInfo,
    UserIdInfo,
    UserList,
)
from .user_list_direct_license import (
    UserListDirectLicense,
)
from .user_list_direct_license_service import (
    CreateUserListDirectLicenseRequest,
    GetUserListDirectLicenseRequest,
    ListUserListDirectLicensesRequest,
    ListUserListDirectLicensesResponse,
    UpdateUserListDirectLicenseRequest,
)
from .user_list_global_license import (
    UserListGlobalLicense,
    UserListGlobalLicenseCustomerInfo,
)
from .user_list_global_license_service import (
    CreateUserListGlobalLicenseRequest,
    GetUserListGlobalLicenseRequest,
    ListUserListGlobalLicenseCustomerInfosRequest,
    ListUserListGlobalLicenseCustomerInfosResponse,
    ListUserListGlobalLicensesRequest,
    ListUserListGlobalLicensesResponse,
    UpdateUserListGlobalLicenseRequest,
)
from .user_list_global_license_type import (
    UserListGlobalLicenseType,
)
from .user_list_license_client_account_type import (
    UserListLicenseClientAccountType,
)
from .user_list_license_metrics import (
    UserListLicenseMetrics,
)
from .user_list_license_pricing import (
    UserListLicensePricing,
)
from .user_list_license_status import (
    UserListLicenseStatus,
)
from .user_list_service import (
    CreateUserListRequest,
    DeleteUserListRequest,
    GetUserListRequest,
    ListUserListsRequest,
    ListUserListsResponse,
    UpdateUserListRequest,
)
from .user_properties import (
    CustomerType,
    CustomerValueBucket,
    UserProperties,
    UserProperty,
)

__all__ = (
    "AgeRange",
    "AudienceMember",
    "MobileData",
    "PairData",
    "PpidData",
    "UserIdData",
    "CartData",
    "Item",
    "Consent",
    "ConsentStatus",
    "Destination",
    "ProductAccount",
    "Product",
    "DeviceInfo",
    "AwsWrappedKeyInfo",
    "EncryptionInfo",
    "GcpWrappedKeyInfo",
    "ErrorReason",
    "AdIdentifiers",
    "CustomVariable",
    "Event",
    "EventParameter",
    "EventSource",
    "ExperimentalField",
    "Gender",
    "IngestAudienceMembersRequest",
    "IngestAudienceMembersResponse",
    "IngestEventsRequest",
    "IngestEventsResponse",
    "RemoveAudienceMembersRequest",
    "RemoveAudienceMembersResponse",
    "RetrieveRequestStatusRequest",
    "RetrieveRequestStatusResponse",
    "Encoding",
    "Baseline",
    "RetrieveInsightsRequest",
    "RetrieveInsightsResponse",
    "ItemParameter",
    "MatchRateRange",
    "CreatePartnerLinkRequest",
    "DeletePartnerLinkRequest",
    "PartnerLink",
    "SearchPartnerLinksRequest",
    "SearchPartnerLinksResponse",
    "ErrorCount",
    "ErrorInfo",
    "WarningCount",
    "WarningInfo",
    "ProcessingErrorReason",
    "ProcessingWarningReason",
    "RequestStatusPerDestination",
    "TermsOfService",
    "TermsOfServiceStatus",
    "AddressInfo",
    "UserData",
    "UserIdentifier",
    "ContactIdInfo",
    "IngestedUserListInfo",
    "MobileIdInfo",
    "PairIdInfo",
    "PartnerAudienceInfo",
    "PseudonymousIdInfo",
    "SizeInfo",
    "TargetNetworkInfo",
    "UserIdInfo",
    "UserList",
    "DataSourceType",
    "UserListDirectLicense",
    "CreateUserListDirectLicenseRequest",
    "GetUserListDirectLicenseRequest",
    "ListUserListDirectLicensesRequest",
    "ListUserListDirectLicensesResponse",
    "UpdateUserListDirectLicenseRequest",
    "UserListGlobalLicense",
    "UserListGlobalLicenseCustomerInfo",
    "CreateUserListGlobalLicenseRequest",
    "GetUserListGlobalLicenseRequest",
    "ListUserListGlobalLicenseCustomerInfosRequest",
    "ListUserListGlobalLicenseCustomerInfosResponse",
    "ListUserListGlobalLicensesRequest",
    "ListUserListGlobalLicensesResponse",
    "UpdateUserListGlobalLicenseRequest",
    "UserListGlobalLicenseType",
    "UserListLicenseClientAccountType",
    "UserListLicenseMetrics",
    "UserListLicensePricing",
    "UserListLicenseStatus",
    "CreateUserListRequest",
    "DeleteUserListRequest",
    "GetUserListRequest",
    "ListUserListsRequest",
    "ListUserListsResponse",
    "UpdateUserListRequest",
    "UserProperties",
    "UserProperty",
    "CustomerType",
    "CustomerValueBucket",
)
