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
from google.maps.solar_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.solar import SolarClient
from .services.solar import SolarAsyncClient

from .types.solar_service import BuildingInsights
from .types.solar_service import CashPurchaseSavings
from .types.solar_service import DataLayers
from .types.solar_service import FinancedPurchaseSavings
from .types.solar_service import FinancialAnalysis
from .types.solar_service import FinancialDetails
from .types.solar_service import FindClosestBuildingInsightsRequest
from .types.solar_service import GetDataLayersRequest
from .types.solar_service import GetGeoTiffRequest
from .types.solar_service import LatLngBox
from .types.solar_service import LeasingSavings
from .types.solar_service import RoofSegmentSizeAndSunshineStats
from .types.solar_service import RoofSegmentSummary
from .types.solar_service import SavingsOverTime
from .types.solar_service import SizeAndSunshineStats
from .types.solar_service import SolarPanel
from .types.solar_service import SolarPanelConfig
from .types.solar_service import SolarPotential
from .types.solar_service import DataLayerView
from .types.solar_service import ImageryQuality
from .types.solar_service import SolarPanelOrientation

__all__ = (
    'SolarAsyncClient',
'BuildingInsights',
'CashPurchaseSavings',
'DataLayerView',
'DataLayers',
'FinancedPurchaseSavings',
'FinancialAnalysis',
'FinancialDetails',
'FindClosestBuildingInsightsRequest',
'GetDataLayersRequest',
'GetGeoTiffRequest',
'ImageryQuality',
'LatLngBox',
'LeasingSavings',
'RoofSegmentSizeAndSunshineStats',
'RoofSegmentSummary',
'SavingsOverTime',
'SizeAndSunshineStats',
'SolarClient',
'SolarPanel',
'SolarPanelConfig',
'SolarPanelOrientation',
'SolarPotential',
)
