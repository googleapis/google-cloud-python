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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
from google.type import datetime_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore
import proto  # type: ignore

from google.maps.weather_v1.types import forecast_day, forecast_hour, history_hour
from google.maps.weather_v1.types import weather_condition as gmw_weather_condition
from google.maps.weather_v1.types import air_pressure as gmw_air_pressure
from google.maps.weather_v1.types import precipitation as gmw_precipitation
from google.maps.weather_v1.types import temperature as gmw_temperature
from google.maps.weather_v1.types import units_system as gmw_units_system
from google.maps.weather_v1.types import visibility as gmw_visibility
from google.maps.weather_v1.types import wind as gmw_wind

__protobuf__ = proto.module(
    package="google.maps.weather.v1",
    manifest={
        "LookupCurrentConditionsRequest",
        "LookupCurrentConditionsResponse",
        "LookupForecastHoursRequest",
        "LookupForecastHoursResponse",
        "LookupForecastDaysRequest",
        "LookupForecastDaysResponse",
        "LookupHistoryHoursRequest",
        "LookupHistoryHoursResponse",
    },
)


class LookupCurrentConditionsRequest(proto.Message):
    r"""Request for the LookupCurrentConditions RPC.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        location (google.type.latlng_pb2.LatLng):
            Required. The location to get the current
            weather conditions for.
        units_system (google.maps.weather_v1.types.UnitsSystem):
            Optional. The units system to use for the
            returned weather conditions. If not provided,
            the returned weather conditions will be in the
            metric system (default = METRIC).
        language_code (str):
            Optional. Allows the client to choose the
            language for the response. If data cannot be
            provided for that language, the API uses the
            closest match. Allowed values rely on the IETF
            BCP-47 standard. The default value is "en".

            This field is a member of `oneof`_ ``_language_code``.
    """

    location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=1,
        message=latlng_pb2.LatLng,
    )
    units_system: gmw_units_system.UnitsSystem = proto.Field(
        proto.ENUM,
        number=2,
        enum=gmw_units_system.UnitsSystem,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )


class LookupCurrentConditionsResponse(proto.Message):
    r"""Response for the LookupCurrentConditions RPC - represents the
    current weather conditions at the requested location.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        current_time (google.protobuf.timestamp_pb2.Timestamp):
            Current time (UTC) associated with the
            returned data.
        time_zone (google.type.datetime_pb2.TimeZone):
            The time zone at the requested location.
        is_daytime (bool):
            True if the current time at the requested
            location is between the local sunrise
            (inclusive) and the sunset (exclusive) times.
            Otherwise, it is nighttime (between the sunset
            and the next sunrise).

            This field is a member of `oneof`_ ``_is_daytime``.
        weather_condition (google.maps.weather_v1.types.WeatherCondition):
            The current weather condition.
        temperature (google.maps.weather_v1.types.Temperature):
            The current temperature.
        feels_like_temperature (google.maps.weather_v1.types.Temperature):
            The measure of how the temperature currently
            feels like at the requested location.
        dew_point (google.maps.weather_v1.types.Temperature):
            The current dew point temperature.
        heat_index (google.maps.weather_v1.types.Temperature):
            The current heat index temperature.
        wind_chill (google.maps.weather_v1.types.Temperature):
            The current wind chill, air temperature
            exposed on the skin.
        relative_humidity (int):
            The current percent of relative humidity
            (values from 0 to 100).

            This field is a member of `oneof`_ ``_relative_humidity``.
        uv_index (int):
            The current ultraviolet (UV) index.

            This field is a member of `oneof`_ ``_uv_index``.
        precipitation (google.maps.weather_v1.types.Precipitation):
            The current precipitation probability and
            amount of precipitation accumulated over the
            last hour.
        thunderstorm_probability (int):
            The current thunderstorm probability (values
            from 0 to 100).

            This field is a member of `oneof`_ ``_thunderstorm_probability``.
        air_pressure (google.maps.weather_v1.types.AirPressure):
            The current air pressure conditions.
        wind (google.maps.weather_v1.types.Wind):
            The current wind conditions.
        visibility (google.maps.weather_v1.types.Visibility):
            The current visibility.
        cloud_cover (int):
            The current percentage of the sky covered by
            clouds (values from 0 to 100).

            This field is a member of `oneof`_ ``_cloud_cover``.
        current_conditions_history (google.maps.weather_v1.types.LookupCurrentConditionsResponse.CurrentConditionsHistory):
            The changes in the current conditions over
            the last 24 hours.
    """

    class CurrentConditionsHistory(proto.Message):
        r"""Represents a set of changes in the current conditions over
        the last 24 hours.

        Attributes:
            temperature_change (google.maps.weather_v1.types.Temperature):
                The current temperature minus the temperature
                24 hours ago.
            max_temperature (google.maps.weather_v1.types.Temperature):
                The maximum (high) temperature in the past 24
                hours.
            min_temperature (google.maps.weather_v1.types.Temperature):
                The minimum (low) temperature in the past 24
                hours.
            qpf (google.maps.weather_v1.types.QuantitativePrecipitationForecast):
                The amount of precipitation (rain or snow),
                measured as liquid water equivalent, that has
                accumulated over the last 24 hours. Note: QPF is
                an abbreviation for Quantitative Precipitation
                Forecast (please see the
                QuantitativePrecipitationForecast definition for
                more details).
        """

        temperature_change: gmw_temperature.Temperature = proto.Field(
            proto.MESSAGE,
            number=1,
            message=gmw_temperature.Temperature,
        )
        max_temperature: gmw_temperature.Temperature = proto.Field(
            proto.MESSAGE,
            number=2,
            message=gmw_temperature.Temperature,
        )
        min_temperature: gmw_temperature.Temperature = proto.Field(
            proto.MESSAGE,
            number=3,
            message=gmw_temperature.Temperature,
        )
        qpf: gmw_precipitation.QuantitativePrecipitationForecast = proto.Field(
            proto.MESSAGE,
            number=6,
            message=gmw_precipitation.QuantitativePrecipitationForecast,
        )

    current_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    time_zone: datetime_pb2.TimeZone = proto.Field(
        proto.MESSAGE,
        number=2,
        message=datetime_pb2.TimeZone,
    )
    is_daytime: bool = proto.Field(
        proto.BOOL,
        number=3,
        optional=True,
    )
    weather_condition: gmw_weather_condition.WeatherCondition = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gmw_weather_condition.WeatherCondition,
    )
    temperature: gmw_temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gmw_temperature.Temperature,
    )
    feels_like_temperature: gmw_temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=6,
        message=gmw_temperature.Temperature,
    )
    dew_point: gmw_temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=7,
        message=gmw_temperature.Temperature,
    )
    heat_index: gmw_temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=8,
        message=gmw_temperature.Temperature,
    )
    wind_chill: gmw_temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=9,
        message=gmw_temperature.Temperature,
    )
    relative_humidity: int = proto.Field(
        proto.INT32,
        number=10,
        optional=True,
    )
    uv_index: int = proto.Field(
        proto.INT32,
        number=11,
        optional=True,
    )
    precipitation: gmw_precipitation.Precipitation = proto.Field(
        proto.MESSAGE,
        number=12,
        message=gmw_precipitation.Precipitation,
    )
    thunderstorm_probability: int = proto.Field(
        proto.INT32,
        number=13,
        optional=True,
    )
    air_pressure: gmw_air_pressure.AirPressure = proto.Field(
        proto.MESSAGE,
        number=14,
        message=gmw_air_pressure.AirPressure,
    )
    wind: gmw_wind.Wind = proto.Field(
        proto.MESSAGE,
        number=15,
        message=gmw_wind.Wind,
    )
    visibility: gmw_visibility.Visibility = proto.Field(
        proto.MESSAGE,
        number=16,
        message=gmw_visibility.Visibility,
    )
    cloud_cover: int = proto.Field(
        proto.INT32,
        number=17,
        optional=True,
    )
    current_conditions_history: CurrentConditionsHistory = proto.Field(
        proto.MESSAGE,
        number=18,
        message=CurrentConditionsHistory,
    )


class LookupForecastHoursRequest(proto.Message):
    r"""Request for the LookupForecastHours RPC.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        location (google.type.latlng_pb2.LatLng):
            Required. The location to get the hourly
            forecast for.
        hours (int):
            Optional. Limits the amount of total hours to
            fetch starting from the current hour - a value
            from 1 to 240 (inclusive). The default is the
            maximum allowed value of 240.

            This field is a member of `oneof`_ ``_hours``.
        units_system (google.maps.weather_v1.types.UnitsSystem):
            Optional. The units system to use for the
            returned weather conditions. If not provided,
            the returned weather conditions will be in the
            metric system (default = METRIC).
        language_code (str):
            Optional. Allows the client to choose the
            language for the response. If data cannot be
            provided for that language, the API uses the
            closest match. Allowed values rely on the IETF
            BCP-47 standard. The default value is "en".

            This field is a member of `oneof`_ ``_language_code``.
        page_size (int):
            Optional. The maximum number of hourly
            forecast records to return per page
            - a value from 1 to 24 (inclusive). The default
              is the maximum allowed value of 24.
        page_token (str):
            Optional. A page token received from a
            previous request. It is used to retrieve the
            subsequent page.
    """

    location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=1,
        message=latlng_pb2.LatLng,
    )
    hours: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )
    units_system: gmw_units_system.UnitsSystem = proto.Field(
        proto.ENUM,
        number=3,
        enum=gmw_units_system.UnitsSystem,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=5,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class LookupForecastHoursResponse(proto.Message):
    r"""Response for the LookupForecastHours RPC.

    Attributes:
        forecast_hours (MutableSequence[google.maps.weather_v1.types.ForecastHour]):
            The hourly forecast records, according to the
            number of hours and page size specified in the
            request.
        time_zone (google.type.datetime_pb2.TimeZone):
            The time zone at the requested location.
        next_page_token (str):
            The token to retrieve the next page.
    """

    @property
    def raw_page(self):
        return self

    forecast_hours: MutableSequence[forecast_hour.ForecastHour] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=forecast_hour.ForecastHour,
    )
    time_zone: datetime_pb2.TimeZone = proto.Field(
        proto.MESSAGE,
        number=2,
        message=datetime_pb2.TimeZone,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class LookupForecastDaysRequest(proto.Message):
    r"""Request for the LookupForecastDays RPC.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        location (google.type.latlng_pb2.LatLng):
            Required. The location to get the daily
            forecast for.
        days (int):
            Optional. Limits the amount of total days to
            fetch starting from the current day - a value
            from 1 to 10 (inclusive). The default value is
            the maximum allowed value of 10.

            This field is a member of `oneof`_ ``_days``.
        units_system (google.maps.weather_v1.types.UnitsSystem):
            Optional. The units system to use for the
            returned weather conditions. If not provided,
            the returned weather conditions will be in the
            metric system (default = METRIC).
        language_code (str):
            Optional. Allows the client to choose the
            language for the response. If data cannot be
            provided for that language, the API uses the
            closest match. Allowed values rely on the IETF
            BCP-47 standard. The default value is "en".

            This field is a member of `oneof`_ ``_language_code``.
        page_size (int):
            Optional. The maximum number of daily
            forecast records to return per page - a value
            from 1 to 10 (inclusive). The default value is
            5.
        page_token (str):
            Optional. A page token received from a
            previous request. It is used to retrieve the
            subsequent page.
    """

    location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=1,
        message=latlng_pb2.LatLng,
    )
    days: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )
    units_system: gmw_units_system.UnitsSystem = proto.Field(
        proto.ENUM,
        number=3,
        enum=gmw_units_system.UnitsSystem,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=5,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class LookupForecastDaysResponse(proto.Message):
    r"""Response for the LookupForecastDays RPC.

    Attributes:
        forecast_days (MutableSequence[google.maps.weather_v1.types.ForecastDay]):
            The daily forecast records, according to the
            number of days and page size specified in the
            request.
        time_zone (google.type.datetime_pb2.TimeZone):
            The time zone at the requested location.
        next_page_token (str):
            The token to retrieve the next page.
    """

    @property
    def raw_page(self):
        return self

    forecast_days: MutableSequence[forecast_day.ForecastDay] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=forecast_day.ForecastDay,
    )
    time_zone: datetime_pb2.TimeZone = proto.Field(
        proto.MESSAGE,
        number=2,
        message=datetime_pb2.TimeZone,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class LookupHistoryHoursRequest(proto.Message):
    r"""Request for the LookupHistoryHours RPC.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        location (google.type.latlng_pb2.LatLng):
            Required. The location to get the hourly
            historical data for.
        hours (int):
            Optional. Limits the amount of total hours to
            fetch starting from the last hour - a from 1 to
            24 (inclusive). The default is the maximum
            allowed value of 24.

            This field is a member of `oneof`_ ``_hours``.
        units_system (google.maps.weather_v1.types.UnitsSystem):
            Optional. The units system to use for the
            returned weather conditions. If not provided,
            the returned weather conditions will be in the
            metric system (default = METRIC).
        language_code (str):
            Optional. Allows the client to choose the
            language for the response. If data cannot be
            provided for that language, the API uses the
            closest match. Allowed values rely on the IETF
            BCP-47 standard. The default value is "en".

            This field is a member of `oneof`_ ``_language_code``.
        page_size (int):
            Optional. The maximum number of hourly
            historical records to return per page - a value
            from 1 to 24 (inclusive). The default is the
            maximum allowed value of 24.
        page_token (str):
            Optional. A page token received from a
            previous request. It is used to retrieve the
            subsequent page.
    """

    location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=1,
        message=latlng_pb2.LatLng,
    )
    hours: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )
    units_system: gmw_units_system.UnitsSystem = proto.Field(
        proto.ENUM,
        number=3,
        enum=gmw_units_system.UnitsSystem,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=5,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class LookupHistoryHoursResponse(proto.Message):
    r"""Response for the LookupHistoryHours RPC.

    Attributes:
        history_hours (MutableSequence[google.maps.weather_v1.types.HistoryHour]):
            The hourly historical records, according to
            the number of hours and page size specified in
            the request.
        time_zone (google.type.datetime_pb2.TimeZone):
            The time zone at the requested location.
        next_page_token (str):
            The token to retrieve the next page.
    """

    @property
    def raw_page(self):
        return self

    history_hours: MutableSequence[history_hour.HistoryHour] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=history_hour.HistoryHour,
    )
    time_zone: datetime_pb2.TimeZone = proto.Field(
        proto.MESSAGE,
        number=2,
        message=datetime_pb2.TimeZone,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
