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
from google.ads.datamanager import gapic_version as package_version

__version__ = package_version.__version__


from google.ads.datamanager_v1.services.ingestion_service.async_client import (
    IngestionServiceAsyncClient,
)
from google.ads.datamanager_v1.services.ingestion_service.client import (
    IngestionServiceClient,
)
from google.ads.datamanager_v1.types.audience import (
    AudienceMember,
    MobileData,
    PairData,
)
from google.ads.datamanager_v1.types.cart_data import CartData, Item
from google.ads.datamanager_v1.types.consent import Consent, ConsentStatus
from google.ads.datamanager_v1.types.destination import (
    Destination,
    Product,
    ProductAccount,
)
from google.ads.datamanager_v1.types.device_info import DeviceInfo
from google.ads.datamanager_v1.types.encryption_info import (
    AwsWrappedKeyInfo,
    EncryptionInfo,
    GcpWrappedKeyInfo,
)
from google.ads.datamanager_v1.types.error import ErrorReason
from google.ads.datamanager_v1.types.event import (
    AdIdentifiers,
    CustomVariable,
    Event,
    EventParameter,
    EventSource,
)
from google.ads.datamanager_v1.types.experimental_field import ExperimentalField
from google.ads.datamanager_v1.types.ingestion_service import (
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
from google.ads.datamanager_v1.types.item_parameter import ItemParameter
from google.ads.datamanager_v1.types.match_rate import MatchRateRange
from google.ads.datamanager_v1.types.processing_errors import (
    ErrorCount,
    ErrorInfo,
    ProcessingErrorReason,
    ProcessingWarningReason,
    WarningCount,
    WarningInfo,
)
from google.ads.datamanager_v1.types.request_status_per_destination import (
    RequestStatusPerDestination,
)
from google.ads.datamanager_v1.types.terms_of_service import (
    TermsOfService,
    TermsOfServiceStatus,
)
from google.ads.datamanager_v1.types.user_data import (
    AddressInfo,
    UserData,
    UserIdentifier,
)
from google.ads.datamanager_v1.types.user_properties import (
    CustomerType,
    CustomerValueBucket,
    UserProperties,
    UserProperty,
)

__all__ = (
    "IngestionServiceClient",
    "IngestionServiceAsyncClient",
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
