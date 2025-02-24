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

from google.type import date_pb2  # type: ignore
from google.type import interval_pb2  # type: ignore
import proto  # type: ignore

from google.maps.weather_v1.types import weather_condition as gmw_weather_condition
from google.maps.weather_v1.types import celestial_events, ice
from google.maps.weather_v1.types import precipitation as gmw_precipitation
from google.maps.weather_v1.types import temperature
from google.maps.weather_v1.types import wind as gmw_wind

__protobuf__ = proto.module(
    package="google.maps.weather.v1",
    manifest={
        "ForecastDay",
        "ForecastDayPart",
    },
)


class ForecastDay(proto.Message):
    r"""Represents a daily forecast record at a given location.

    Attributes:
        interval (google.type.interval_pb2.Interval):
            The UTC time interval when this forecasted day is starts
            (inclusive) and ends (exclusive). Note: a day starts at 7am
            and ends at 7am next day, local time. For example: If the
            local time zone is UTC-7, then the interval will start at
            the time ``14:00:00.000Z`` and end at the same hour the next
            day.
        display_date (google.type.date_pb2.Date):
            The local date in the time zone of the
            location (civil time) which this daily forecast
            is calculated for. This field may be used for
            display purposes on the client.
        daytime_forecast (google.maps.weather_v1.types.ForecastDayPart):
            The forecasted weather conditions for the
            daytime part of the day (7am to 7pm local time).
        nighttime_forecast (google.maps.weather_v1.types.ForecastDayPart):
            The forecasted weather conditions for the
            nighttime part of the day (7pm to 7am next day,
            local time).
        max_temperature (google.maps.weather_v1.types.Temperature):
            The maximum (high) temperature throughout the
            day.
        min_temperature (google.maps.weather_v1.types.Temperature):
            The minimum (low) temperature throughout the
            day.
        feels_like_max_temperature (google.maps.weather_v1.types.Temperature):
            The maximum (high) feels-like temperature
            throughout the day.
        feels_like_min_temperature (google.maps.weather_v1.types.Temperature):
            The minimum (low) feels-like temperature
            throughout the day.
        max_heat_index (google.maps.weather_v1.types.Temperature):
            The maximum heat index temperature throughout
            the day.
        sun_events (google.maps.weather_v1.types.SunEvents):
            The events related to the sun (e.g. sunrise,
            sunset).
        moon_events (google.maps.weather_v1.types.MoonEvents):
            The events related to the moon (e.g.
            moonrise, moonset).
    """

    interval: interval_pb2.Interval = proto.Field(
        proto.MESSAGE,
        number=1,
        message=interval_pb2.Interval,
    )
    display_date: date_pb2.Date = proto.Field(
        proto.MESSAGE,
        number=2,
        message=date_pb2.Date,
    )
    daytime_forecast: "ForecastDayPart" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ForecastDayPart",
    )
    nighttime_forecast: "ForecastDayPart" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="ForecastDayPart",
    )
    max_temperature: temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=5,
        message=temperature.Temperature,
    )
    min_temperature: temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=6,
        message=temperature.Temperature,
    )
    feels_like_max_temperature: temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=7,
        message=temperature.Temperature,
    )
    feels_like_min_temperature: temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=8,
        message=temperature.Temperature,
    )
    max_heat_index: temperature.Temperature = proto.Field(
        proto.MESSAGE,
        number=11,
        message=temperature.Temperature,
    )
    sun_events: celestial_events.SunEvents = proto.Field(
        proto.MESSAGE,
        number=9,
        message=celestial_events.SunEvents,
    )
    moon_events: celestial_events.MoonEvents = proto.Field(
        proto.MESSAGE,
        number=10,
        message=celestial_events.MoonEvents,
    )


class ForecastDayPart(proto.Message):
    r"""Represents a forecast record for a part of the day.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        interval (google.type.interval_pb2.Interval):
            The UTC date and time when this part of the day starts
            (inclusive) and ends (exclusive). Note: a part of a day
            starts at 7am and ends at 7pm the same day, local time. For
            example: If the local time zone is UTC-7, then the daytime
            interval will start at the time ``14:00:00.000Z`` and end at
            ``02:00:00.000Z`` the next day and the nighttime interval
            will start at ``02:00:00.000Z`` the next day and end at
            ``14:00:00.000Z`` that same day.
        weather_condition (google.maps.weather_v1.types.WeatherCondition):
            The forecasted weather condition.
        relative_humidity (int):
            The forecasted percent of relative humidity
            (values from 0 to 100).

            This field is a member of `oneof`_ ``_relative_humidity``.
        uv_index (int):
            The maximum forecasted ultraviolet (UV)
            index.

            This field is a member of `oneof`_ ``_uv_index``.
        precipitation (google.maps.weather_v1.types.Precipitation):
            The forecasted precipitation.
        thunderstorm_probability (int):
            The average thunderstorm probability.

            This field is a member of `oneof`_ ``_thunderstorm_probability``.
        wind (google.maps.weather_v1.types.Wind):
            The average wind direction and maximum speed
            and gust.
        cloud_cover (int):
            Average cloud cover percent.

            This field is a member of `oneof`_ ``_cloud_cover``.
        ice_thickness (google.maps.weather_v1.types.IceThickness):
            The accumulated amount of ice for the part of
            the day.
    """

    interval: interval_pb2.Interval = proto.Field(
        proto.MESSAGE,
        number=1,
        message=interval_pb2.Interval,
    )
    weather_condition: gmw_weather_condition.WeatherCondition = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gmw_weather_condition.WeatherCondition,
    )
    relative_humidity: int = proto.Field(
        proto.INT32,
        number=3,
        optional=True,
    )
    uv_index: int = proto.Field(
        proto.INT32,
        number=4,
        optional=True,
    )
    precipitation: gmw_precipitation.Precipitation = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gmw_precipitation.Precipitation,
    )
    thunderstorm_probability: int = proto.Field(
        proto.INT32,
        number=6,
        optional=True,
    )
    wind: gmw_wind.Wind = proto.Field(
        proto.MESSAGE,
        number=7,
        message=gmw_wind.Wind,
    )
    cloud_cover: int = proto.Field(
        proto.INT32,
        number=8,
        optional=True,
    )
    ice_thickness: ice.IceThickness = proto.Field(
        proto.MESSAGE,
        number=9,
        message=ice.IceThickness,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
