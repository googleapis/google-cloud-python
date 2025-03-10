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
from google.maps.solar import gapic_version as package_version

__version__ = package_version.__version__


from google.maps.solar_v1.services.solar.client import SolarClient
from google.maps.solar_v1.services.solar.async_client import SolarAsyncClient

from google.maps.solar_v1.types.solar_service import BuildingInsights
from google.maps.solar_v1.types.solar_service import CashPurchaseSavings
from google.maps.solar_v1.types.solar_service import DataLayers
from google.maps.solar_v1.types.solar_service import FinancedPurchaseSavings
from google.maps.solar_v1.types.solar_service import FinancialAnalysis
from google.maps.solar_v1.types.solar_service import FinancialDetails
from google.maps.solar_v1.types.solar_service import FindClosestBuildingInsightsRequest
from google.maps.solar_v1.types.solar_service import GetDataLayersRequest
from google.maps.solar_v1.types.solar_service import GetGeoTiffRequest
from google.maps.solar_v1.types.solar_service import LatLngBox
from google.maps.solar_v1.types.solar_service import LeasingSavings
from google.maps.solar_v1.types.solar_service import RoofSegmentSizeAndSunshineStats
from google.maps.solar_v1.types.solar_service import RoofSegmentSummary
from google.maps.solar_v1.types.solar_service import SavingsOverTime
from google.maps.solar_v1.types.solar_service import SizeAndSunshineStats
from google.maps.solar_v1.types.solar_service import SolarPanel
from google.maps.solar_v1.types.solar_service import SolarPanelConfig
from google.maps.solar_v1.types.solar_service import SolarPotential
from google.maps.solar_v1.types.solar_service import DataLayerView
from google.maps.solar_v1.types.solar_service import ImageryQuality
from google.maps.solar_v1.types.solar_service import SolarPanelOrientation

__all__ = ('SolarClient',
    'SolarAsyncClient',
    'BuildingInsights',
    'CashPurchaseSavings',
    'DataLayers',
    'FinancedPurchaseSavings',
    'FinancialAnalysis',
    'FinancialDetails',
    'FindClosestBuildingInsightsRequest',
    'GetDataLayersRequest',
    'GetGeoTiffRequest',
    'LatLngBox',
    'LeasingSavings',
    'RoofSegmentSizeAndSunshineStats',
    'RoofSegmentSummary',
    'SavingsOverTime',
    'SizeAndSunshineStats',
    'SolarPanel',
    'SolarPanelConfig',
    'SolarPotential',
    'DataLayerView',
    'ImageryQuality',
    'SolarPanelOrientation',
)
