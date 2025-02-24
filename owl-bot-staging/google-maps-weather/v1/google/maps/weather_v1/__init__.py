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
from google.maps.weather_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.weather import WeatherClient
from .services.weather import WeatherAsyncClient

from .types.air_pressure import AirPressure
from .types.celestial_events import MoonEvents
from .types.celestial_events import SunEvents
from .types.celestial_events import MoonPhase
from .types.forecast_day import ForecastDay
from .types.forecast_day import ForecastDayPart
from .types.forecast_hour import ForecastHour
from .types.history_hour import HistoryHour
from .types.ice import IceThickness
from .types.precipitation import Precipitation
from .types.precipitation import PrecipitationProbability
from .types.precipitation import QuantitativePrecipitationForecast
from .types.precipitation import PrecipitationType
from .types.temperature import Temperature
from .types.temperature import TemperatureUnit
from .types.units_system import UnitsSystem
from .types.visibility import Visibility
from .types.weather_condition import WeatherCondition
from .types.weather_service import LookupCurrentConditionsRequest
from .types.weather_service import LookupCurrentConditionsResponse
from .types.weather_service import LookupForecastDaysRequest
from .types.weather_service import LookupForecastDaysResponse
from .types.weather_service import LookupForecastHoursRequest
from .types.weather_service import LookupForecastHoursResponse
from .types.weather_service import LookupHistoryHoursRequest
from .types.weather_service import LookupHistoryHoursResponse
from .types.wind import Wind
from .types.wind import WindDirection
from .types.wind import WindSpeed
from .types.wind import CardinalDirection
from .types.wind import SpeedUnit

__all__ = (
    'WeatherAsyncClient',
'AirPressure',
'CardinalDirection',
'ForecastDay',
'ForecastDayPart',
'ForecastHour',
'HistoryHour',
'IceThickness',
'LookupCurrentConditionsRequest',
'LookupCurrentConditionsResponse',
'LookupForecastDaysRequest',
'LookupForecastDaysResponse',
'LookupForecastHoursRequest',
'LookupForecastHoursResponse',
'LookupHistoryHoursRequest',
'LookupHistoryHoursResponse',
'MoonEvents',
'MoonPhase',
'Precipitation',
'PrecipitationProbability',
'PrecipitationType',
'QuantitativePrecipitationForecast',
'SpeedUnit',
'SunEvents',
'Temperature',
'TemperatureUnit',
'UnitsSystem',
'Visibility',
'WeatherClient',
'WeatherCondition',
'Wind',
'WindDirection',
'WindSpeed',
)
