# Copyright (C) 2020  Google LLC
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

import pytest

import proto
from google.protobuf.json_format import MessageToJson, Parse, ParseError


def test_message_to_json():
    class Squid(proto.Message):
        mass_kg = proto.Field(proto.INT32, number=1)

    s = Squid(mass_kg=100)
    json = Squid.to_json(s)
    json = json.replace(" ", "").replace("\n", "")
    assert json == '{"massKg":100}'


def test_message_from_json():
    class Squid(proto.Message):
        mass_kg = proto.Field(proto.INT32, number=1)

    json = """{
    "massKg": 100
    }
    """

    s = Squid.from_json(json)
    assert s == Squid(mass_kg=100)


def test_message_json_round_trip():
    class Squid(proto.Message):
        mass_kg = proto.Field(proto.INT32, number=1)

    s = Squid(mass_kg=100)
    json = Squid.to_json(s)
    s2 = Squid.from_json(json)

    assert s == s2


def test_json_stringy_enums():
    class Squid(proto.Message):
        zone = proto.Field(proto.ENUM, number=1, enum="Zone")

    class Zone(proto.Enum):
        EPIPELAGIC = 0
        MESOPELAGIC = 1
        BATHYPELAGIC = 2
        ABYSSOPELAGIC = 3

    s1 = Squid(zone=Zone.MESOPELAGIC)
    json = (
        Squid.to_json(s1, use_integers_for_enums=False)
        .replace(" ", "")
        .replace("\n", "")
    )
    assert json == '{"zone":"MESOPELAGIC"}'

    s2 = Squid.from_json(json)
    assert s2.zone == s1.zone


def test_json_default_enums():
    class Squid(proto.Message):
        zone = proto.Field(proto.ENUM, number=1, enum="Zone")

    class Zone(proto.Enum):
        EPIPELAGIC = 0
        MESOPELAGIC = 1
        BATHYPELAGIC = 2
        ABYSSOPELAGIC = 3

    s = Squid()
    assert s.zone == Zone.EPIPELAGIC
    json1 = Squid.to_json(s).replace(" ", "").replace("\n", "")
    assert json1 == '{"zone":0}'

    json2 = (
        Squid.to_json(s, use_integers_for_enums=False)
        .replace(" ", "")
        .replace("\n", "")
    )
    assert json2 == '{"zone":"EPIPELAGIC"}'


def test_json_unknown_field():
    # Note that 'lengthCm' is unknown in the local definition.
    # This could happen if the client is using an older proto definition
    # than the server.
    json_str = '{\n  "massKg": 20,\n  "lengthCm": 100\n}'

    class Octopus(proto.Message):
        mass_kg = proto.Field(proto.INT32, number=1)

    o = Octopus.from_json(json_str, ignore_unknown_fields=True)
    assert not hasattr(o, "length_cm")
    assert not hasattr(o, "lengthCm")

    # Don't permit unknown fields by default
    with pytest.raises(ParseError):
        o = Octopus.from_json(json_str)
