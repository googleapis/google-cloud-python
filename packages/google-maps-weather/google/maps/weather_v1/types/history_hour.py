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

from google.type import datetime_pb2  # type: ignore
from google.type import interval_pb2  # type: ignore
import proto  # type: ignore

from google.maps.weather_v1.types import weather_condition as gmw_weather_condition
from google.maps.weather_v1.types import air_pressure as gmw_air_pressure
from google.maps.weather_v1.types import ice
from google.maps.weather_v1.types import precipitation as gmw_precipitation
from google.maps.weather_v1.types import temperature as gmw_temperature
from google.maps.weather_v1.types import visibility as gmw_visibility
from google.maps.weather_v1.types import wind as gmw_wind

__protobuf__ = proto.module(
    package="google.maps.weather.v1",
    manifest={
        "HistoryHour",
    },
)


class HistoryHour(proto.Message):
    r"""Represents an hourly history record at a given location.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        interval (google.type.interval_pb2.Interval):
            The one hour interval (in UTC time) this
            historical data is valid for (the timestamps are
            rounded down to the closest hour).
        display_date_time (google.type.datetime_pb2.DateTime):
            The local date and time in the time zone of
            the location (civil time) which this hourly
            record is calculated for. This field may be used
            for display purposes on the client.
            Note: this date will consist of the year, month,
            day, hour and offset from UTC.
        is_daytime (bool):
            True if this hour is between the local sunrise (inclusive)
            and sunset (exclusive) times. Otherwise, it is nighttime
            (between the sunset and the next sunrise). Note: this hour
            will be considered as daytime or nighttime if the interval
            intersects with the local sunrise and sunset times
            respectively (e.g.: if the interval is from 5am to 6am and
            sunrise is at 5:59am, then is_daytime will be true).

            This field is a member of `oneof`_ ``_is_daytime``.
        weather_condition (google.maps.weather_v1.types.WeatherCondition):
            The historical weather condition.
        temperature (google.maps.weather_v1.types.Temperature):
            The historical temperature.
        feels_like_temperature (google.maps.weather_v1.types.Temperature):
            The measure of how the temperature felt like
            at the requested location.
        dew_point (google.maps.weather_v1.types.Temperature):
            The historical dew point temperature.
        heat_index (google.maps.weather_v1.types.Temperature):
            The historical heat index temperature.
        wind_chill (google.maps.weather_v1.types.Temperature):
            The historical wind chill, air temperature
            exposed on the skin.
        wet_bulb_temperature (google.maps.weather_v1.types.Temperature):
            The historical wet bulb temperature, lowest
            temperature achievable by evaporating water.
        relative_humidity (int):
            The historical percent of relative humidity
            (values from 0 to 100).

            This field is a member of `oneof`_ ``_relative_humidity``.
        uv_index (int):
            The historical ultraviolet (UV) index.

            This field is a member of `oneof`_ ``_uv_index``.
        precipitation (google.maps.weather_v1.types.Precipitation):
            The historical precipitation probability and
            amount of precipitation accumulated over the
            last hour.
        thunderstorm_probability (int):
            The historical thunderstorm probability
            (values from 0 to 100).

            This field is a member of `oneof`_ ``_thunderstorm_probability``.
        air_pressure (google.maps.weather_v1.types.AirPressure):
            The historical air pressure conditions.
        wind (google.maps.weather_v1.types.Wind):
            The historical wind conditions.
        visibility (google.maps.weather_v1.types.Visibility):
            The historical visibility.
        cloud_cover (int):
            The historical percentage of the sky covered
            by clouds (values from 0 to 100).

            This field is a member of `oneof`_ ``_cloud_cover``.
        ice_thickness (google.maps.weather_v1.types.IceThickness):
            The historical ice thickness.
    """

    interval: interval_pb2.Interval = proto.Field(
        proto.MESSAGE,
        number=1,
        message=interval_pb2.Interval,
    )
    display_date_time: datetime_pb2.DateTime = proto.Field(
        proto.MESSAGE,
        number=2,
        message=datetime_pb2.DateTime,
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
    wet_bulb_temperature: gmw_temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=10,
        message=gmw_temperature.Temperature,
    )
    relative_humidity: int = proto.Field(
        proto.INT32,
        number=11,
        optional=True,
    )
    uv_index: int = proto.Field(
        proto.INT32,
        number=12,
        optional=True,
    )
    precipitation: gmw_precipitation.Precipitation = proto.Field(
        proto.MESSAGE,
        number=13,
        message=gmw_precipitation.Precipitation,
    )
    thunderstorm_probability: int = proto.Field(
        proto.INT32,
        number=14,
        optional=True,
    )
    air_pressure: gmw_air_pressure.AirPressure = proto.Field(
        proto.MESSAGE,
        number=15,
        message=gmw_air_pressure.AirPressure,
    )
    wind: gmw_wind.Wind = proto.Field(
        proto.MESSAGE,
        number=16,
        message=gmw_wind.Wind,
    )
    visibility: gmw_visibility.Visibility = proto.Field(
        proto.MESSAGE,
        number=17,
        message=gmw_visibility.Visibility,
    )
    cloud_cover: int = proto.Field(
        proto.INT32,
        number=18,
        optional=True,
    )
    ice_thickness: ice.IceThickness = proto.Field(
        proto.MESSAGE,
        number=19,
        message=ice.IceThickness,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
