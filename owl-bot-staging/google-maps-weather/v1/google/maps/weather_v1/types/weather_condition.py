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

import proto  # type: ignore

from google.type import localized_text_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.maps.weather.v1',
    manifest={
        'WeatherCondition',
    },
)


class WeatherCondition(proto.Message):
    r"""Represents a weather condition for a given location at a
    given period of time.

    Disclaimer: Weather icons and condition codes are subject to
    change. Google may introduce new codes and icons or update
    existing ones as needed. We encourage you to refer to this
    documentation regularly for the most up-to-date information.

    Attributes:
        icon_base_uri (str):
            The base URI for the icon not including the file type
            extension. To display the icon, append a theme if desired
            and the file type extension (``.png`` or ``.svg``) to this
            URI. By default, the icon is light themed, but ``_dark`` can
            be appended for dark mode. For example:
            "https://maps.gstatic.com/weather/v1/dust.svg" or
            "https://maps.gstatic.com/weather/v1/dust_dark.svg", where
            ``icon_base_uri`` is
            "https://maps.gstatic.com/weather/v1/dust".
        description (google.type.localized_text_pb2.LocalizedText):
            The textual description for this weather
            condition (localized).
        type_ (google.maps.weather_v1.types.WeatherCondition.Type):
            The type of weather condition.
    """
    class Type(proto.Enum):
        r"""Marks the weather condition type in a forecast element's
        context.

        Values:
            TYPE_UNSPECIFIED (0):
                The weather condition is unspecified.
            CLEAR (1):
                No clouds.
            MOSTLY_CLEAR (2):
                Periodic clouds.
            PARTLY_CLOUDY (3):
                Party cloudy (some clouds).
            MOSTLY_CLOUDY (4):
                Mostly cloudy (more clouds than sun).
            CLOUDY (5):
                Cloudy (all clouds, no sun).
            WINDY (6):
                High wind.
            WIND_AND_RAIN (7):
                High wind with precipitation.
            LIGHT_RAIN_SHOWERS (8):
                Light intermittent rain.
            CHANCE_OF_SHOWERS (9):
                Chance of intermittent rain.
            SCATTERED_SHOWERS (10):
                Intermittent rain.
            RAIN_SHOWERS (12):
                Showers are considered to be rainfall that
                has a shorter duration than rain, and is
                characterized by suddenness in terms of start
                and stop times, and rapid changes in intensity.
            HEAVY_RAIN_SHOWERS (13):
                Intense showers.
            LIGHT_TO_MODERATE_RAIN (14):
                Rain (light to moderate in quantity).
            MODERATE_TO_HEAVY_RAIN (15):
                Rain (moderate to heavy in quantity).
            RAIN (16):
                Moderate rain.
            LIGHT_RAIN (17):
                Light rain.
            HEAVY_RAIN (18):
                Heavy rain.
            RAIN_PERIODICALLY_HEAVY (19):
                Rain periodically heavy.
            LIGHT_SNOW_SHOWERS (20):
                Light snow that is falling at varying
                intensities for brief periods of time.
            CHANCE_OF_SNOW_SHOWERS (21):
                Chance of snow showers.
            SCATTERED_SNOW_SHOWERS (22):
                Snow that is falling at varying intensities
                for brief periods of time.
            SNOW_SHOWERS (23):
                Snow showers.
            HEAVY_SNOW_SHOWERS (24):
                Heavy snow showers.
            LIGHT_TO_MODERATE_SNOW (25):
                Light to moderate snow.
            MODERATE_TO_HEAVY_SNOW (26):
                Moderate to heavy snow.
            SNOW (27):
                Moderate snow.
            LIGHT_SNOW (28):
                Light snow.
            HEAVY_SNOW (29):
                Heavy snow.
            SNOWSTORM (30):
                Snow with possible thunder and lightning.
            SNOW_PERIODICALLY_HEAVY (31):
                Snow, at times heavy.
            HEAVY_SNOW_STORM (32):
                Heavy snow with possible thunder and
                lightning.
            BLOWING_SNOW (33):
                Snow with intense wind.
            RAIN_AND_SNOW (34):
                Rain and snow mix.
            HAIL (35):
                Hail.
            HAIL_SHOWERS (36):
                Hail that is falling at varying intensities
                for brief periods of time.
            THUNDERSTORM (37):
                Thunderstorm.
            THUNDERSHOWER (38):
                A shower of rain accompanied by thunder and
                lightning.
            LIGHT_THUNDERSTORM_RAIN (39):
                Light thunderstorm rain.
            SCATTERED_THUNDERSTORMS (40):
                Thunderstorms that has rain in various
                intensities for brief periods of time.
            HEAVY_THUNDERSTORM (41):
                Heavy thunderstorm.
        """
        TYPE_UNSPECIFIED = 0
        CLEAR = 1
        MOSTLY_CLEAR = 2
        PARTLY_CLOUDY = 3
        MOSTLY_CLOUDY = 4
        CLOUDY = 5
        WINDY = 6
        WIND_AND_RAIN = 7
        LIGHT_RAIN_SHOWERS = 8
        CHANCE_OF_SHOWERS = 9
        SCATTERED_SHOWERS = 10
        RAIN_SHOWERS = 12
        HEAVY_RAIN_SHOWERS = 13
        LIGHT_TO_MODERATE_RAIN = 14
        MODERATE_TO_HEAVY_RAIN = 15
        RAIN = 16
        LIGHT_RAIN = 17
        HEAVY_RAIN = 18
        RAIN_PERIODICALLY_HEAVY = 19
        LIGHT_SNOW_SHOWERS = 20
        CHANCE_OF_SNOW_SHOWERS = 21
        SCATTERED_SNOW_SHOWERS = 22
        SNOW_SHOWERS = 23
        HEAVY_SNOW_SHOWERS = 24
        LIGHT_TO_MODERATE_SNOW = 25
        MODERATE_TO_HEAVY_SNOW = 26
        SNOW = 27
        LIGHT_SNOW = 28
        HEAVY_SNOW = 29
        SNOWSTORM = 30
        SNOW_PERIODICALLY_HEAVY = 31
        HEAVY_SNOW_STORM = 32
        BLOWING_SNOW = 33
        RAIN_AND_SNOW = 34
        HAIL = 35
        HAIL_SHOWERS = 36
        THUNDERSTORM = 37
        THUNDERSHOWER = 38
        LIGHT_THUNDERSTORM_RAIN = 39
        SCATTERED_THUNDERSTORMS = 40
        HEAVY_THUNDERSTORM = 41

    icon_base_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: localized_text_pb2.LocalizedText = proto.Field(
        proto.MESSAGE,
        number=2,
        message=localized_text_pb2.LocalizedText,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=3,
        enum=Type,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
