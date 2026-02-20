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
from .audience import (
    AudienceMember,
    MobileData,
    PairData,
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
from .item_parameter import (
    ItemParameter,
)
from .match_rate import (
    MatchRateRange,
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
from .user_properties import (
    CustomerType,
    CustomerValueBucket,
    UserProperties,
    UserProperty,
)

__all__ = (
    "AudienceMember",
    "MobileData",
    "PairData",
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
    "IngestAudienceMembersRequest",
    "IngestAudienceMembersResponse",
    "IngestEventsRequest",
    "IngestEventsResponse",
    "RemoveAudienceMembersRequest",
    "RemoveAudienceMembersResponse",
    "RetrieveRequestStatusRequest",
    "RetrieveRequestStatusResponse",
    "Encoding",
    "ItemParameter",
    "MatchRateRange",
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
    "UserProperties",
    "UserProperty",
    "CustomerType",
    "CustomerValueBucket",
)
