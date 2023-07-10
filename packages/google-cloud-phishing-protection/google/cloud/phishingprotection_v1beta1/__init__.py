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
from google.cloud.phishingprotection_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.phishing_protection_service_v1_beta1 import (
    PhishingProtectionServiceV1Beta1AsyncClient,
    PhishingProtectionServiceV1Beta1Client,
)
from .types.phishingprotection import ReportPhishingRequest, ReportPhishingResponse

__all__ = (
    "PhishingProtectionServiceV1Beta1AsyncClient",
    "PhishingProtectionServiceV1Beta1Client",
    "ReportPhishingRequest",
    "ReportPhishingResponse",
)
