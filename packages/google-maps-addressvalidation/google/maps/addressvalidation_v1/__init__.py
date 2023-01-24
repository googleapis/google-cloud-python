# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.maps.addressvalidation_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.address_validation import (
    AddressValidationAsyncClient,
    AddressValidationClient,
)
from .types.address import Address, AddressComponent, ComponentName
from .types.address_validation_service import (
    ProvideValidationFeedbackRequest,
    ProvideValidationFeedbackResponse,
    ValidateAddressRequest,
    ValidateAddressResponse,
    ValidationResult,
    Verdict,
)
from .types.geocode import Geocode, PlusCode
from .types.metadata_ import AddressMetadata
from .types.usps_data import UspsAddress, UspsData

__all__ = (
    "AddressValidationAsyncClient",
    "Address",
    "AddressComponent",
    "AddressMetadata",
    "AddressValidationClient",
    "ComponentName",
    "Geocode",
    "PlusCode",
    "ProvideValidationFeedbackRequest",
    "ProvideValidationFeedbackResponse",
    "UspsAddress",
    "UspsData",
    "ValidateAddressRequest",
    "ValidateAddressResponse",
    "ValidationResult",
    "Verdict",
)
