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
from google.ads.datamanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.ingestion_service import (
    IngestionServiceAsyncClient,
    IngestionServiceClient,
)
from .types.audience import AudienceMember, MobileData, PairData
from .types.cart_data import CartData, Item
from .types.consent import Consent, ConsentStatus
from .types.destination import Destination, Product, ProductAccount
from .types.device_info import DeviceInfo
from .types.encryption_info import AwsWrappedKeyInfo, EncryptionInfo, GcpWrappedKeyInfo
from .types.error import ErrorReason
from .types.event import (
    AdIdentifiers,
    CustomVariable,
    Event,
    EventParameter,
    EventSource,
)
from .types.experimental_field import ExperimentalField
from .types.ingestion_service import (
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
from .types.item_parameter import ItemParameter
from .types.match_rate import MatchRateRange
from .types.processing_errors import (
    ErrorCount,
    ErrorInfo,
    ProcessingErrorReason,
    ProcessingWarningReason,
    WarningCount,
    WarningInfo,
)
from .types.request_status_per_destination import RequestStatusPerDestination
from .types.terms_of_service import TermsOfService, TermsOfServiceStatus
from .types.user_data import AddressInfo, UserData, UserIdentifier
from .types.user_properties import (
    CustomerType,
    CustomerValueBucket,
    UserProperties,
    UserProperty,
)

__all__ = (
    "IngestionServiceAsyncClient",
    "AdIdentifiers",
    "AddressInfo",
    "AudienceMember",
    "AwsWrappedKeyInfo",
    "CartData",
    "Consent",
    "ConsentStatus",
    "CustomVariable",
    "CustomerType",
    "CustomerValueBucket",
    "Destination",
    "DeviceInfo",
    "Encoding",
    "EncryptionInfo",
    "ErrorCount",
    "ErrorInfo",
    "ErrorReason",
    "Event",
    "EventParameter",
    "EventSource",
    "ExperimentalField",
    "GcpWrappedKeyInfo",
    "IngestAudienceMembersRequest",
    "IngestAudienceMembersResponse",
    "IngestEventsRequest",
    "IngestEventsResponse",
    "IngestionServiceClient",
    "Item",
    "ItemParameter",
    "MatchRateRange",
    "MobileData",
    "PairData",
    "ProcessingErrorReason",
    "ProcessingWarningReason",
    "Product",
    "ProductAccount",
    "RemoveAudienceMembersRequest",
    "RemoveAudienceMembersResponse",
    "RequestStatusPerDestination",
    "RetrieveRequestStatusRequest",
    "RetrieveRequestStatusResponse",
    "TermsOfService",
    "TermsOfServiceStatus",
    "UserData",
    "UserIdentifier",
    "UserProperties",
    "UserProperty",
    "WarningCount",
    "WarningInfo",
)
