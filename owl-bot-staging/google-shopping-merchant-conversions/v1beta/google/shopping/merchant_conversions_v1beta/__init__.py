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
from google.shopping.merchant_conversions_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.conversion_sources_service import ConversionSourcesServiceClient
from .services.conversion_sources_service import ConversionSourcesServiceAsyncClient

from .types.conversionsources import AttributionSettings
from .types.conversionsources import ConversionSource
from .types.conversionsources import CreateConversionSourceRequest
from .types.conversionsources import DeleteConversionSourceRequest
from .types.conversionsources import GetConversionSourceRequest
from .types.conversionsources import GoogleAnalyticsLink
from .types.conversionsources import ListConversionSourcesRequest
from .types.conversionsources import ListConversionSourcesResponse
from .types.conversionsources import MerchantCenterDestination
from .types.conversionsources import UndeleteConversionSourceRequest
from .types.conversionsources import UpdateConversionSourceRequest

__all__ = (
    'ConversionSourcesServiceAsyncClient',
'AttributionSettings',
'ConversionSource',
'ConversionSourcesServiceClient',
'CreateConversionSourceRequest',
'DeleteConversionSourceRequest',
'GetConversionSourceRequest',
'GoogleAnalyticsLink',
'ListConversionSourcesRequest',
'ListConversionSourcesResponse',
'MerchantCenterDestination',
'UndeleteConversionSourceRequest',
'UpdateConversionSourceRequest',
)
