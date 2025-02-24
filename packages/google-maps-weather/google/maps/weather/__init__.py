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
from google.maps.weather import gapic_version as package_version

__version__ = package_version.__version__


from google.maps.weather_v1.services.weather.async_client import WeatherAsyncClient
from google.maps.weather_v1.services.weather.client import WeatherClient
from google.maps.weather_v1.types.air_pressure import AirPressure
from google.maps.weather_v1.types.celestial_events import (
    MoonEvents,
    MoonPhase,
    SunEvents,
)
from google.maps.weather_v1.types.forecast_day import ForecastDay, ForecastDayPart
from google.maps.weather_v1.types.forecast_hour import ForecastHour
from google.maps.weather_v1.types.history_hour import HistoryHour
from google.maps.weather_v1.types.ice import IceThickness
from google.maps.weather_v1.types.precipitation import (
    Precipitation,
    PrecipitationProbability,
    PrecipitationType,
    QuantitativePrecipitationForecast,
)
from google.maps.weather_v1.types.temperature import Temperature, TemperatureUnit
from google.maps.weather_v1.types.units_system import UnitsSystem
from google.maps.weather_v1.types.visibility import Visibility
from google.maps.weather_v1.types.weather_condition import WeatherCondition
from google.maps.weather_v1.types.weather_service import (
    LookupCurrentConditionsRequest,
    LookupCurrentConditionsResponse,
    LookupForecastDaysRequest,
    LookupForecastDaysResponse,
    LookupForecastHoursRequest,
    LookupForecastHoursResponse,
    LookupHistoryHoursRequest,
    LookupHistoryHoursResponse,
)
from google.maps.weather_v1.types.wind import (
    CardinalDirection,
    SpeedUnit,
    Wind,
    WindDirection,
    WindSpeed,
)

__all__ = (
    "WeatherClient",
    "WeatherAsyncClient",
    "AirPressure",
    "MoonEvents",
    "SunEvents",
    "MoonPhase",
    "ForecastDay",
    "ForecastDayPart",
    "ForecastHour",
    "HistoryHour",
    "IceThickness",
    "Precipitation",
    "PrecipitationProbability",
    "QuantitativePrecipitationForecast",
    "PrecipitationType",
    "Temperature",
    "TemperatureUnit",
    "UnitsSystem",
    "Visibility",
    "WeatherCondition",
    "LookupCurrentConditionsRequest",
    "LookupCurrentConditionsResponse",
    "LookupForecastDaysRequest",
    "LookupForecastDaysResponse",
    "LookupForecastHoursRequest",
    "LookupForecastHoursResponse",
    "LookupHistoryHoursRequest",
    "LookupHistoryHoursResponse",
    "Wind",
    "WindDirection",
    "WindSpeed",
    "CardinalDirection",
    "SpeedUnit",
)
