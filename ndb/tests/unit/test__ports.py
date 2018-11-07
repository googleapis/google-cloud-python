# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest.mock

import pytest

from google.cloud.ndb import _ports
from google.cloud.ndb import exceptions


class TestGeoPt:
    @staticmethod
    def test_constructor():
        geo_pt = _ports.GeoPt(1.0, 2.0)
        assert geo_pt.lat == 1.0
        assert geo_pt.lon == 2.0

    @staticmethod
    def test_constructor_as_str():
        geo_pt = _ports.GeoPt("-18,100")
        assert geo_pt.lat == -18.0
        assert geo_pt.lon == 100.0

    @staticmethod
    def test_constructor_invalid_str():
        values = ("-18,100,38", None, "foo", 88.0)
        for value in values:
            with pytest.raises(exceptions.BadValueError):
                _ports.GeoPt(value)

    @staticmethod
    def test_constructor_invalid_floats():
        inputs = ((-200, 0), ("x", 0.0), (0.0, "x"), (0.0, 500))
        for latitude, longitude in inputs:
            with pytest.raises(exceptions.BadValueError):
                _ports.GeoPt(latitude, longitude)

    @staticmethod
    def test___eq__():
        geo_pt1 = _ports.GeoPt(-18, 100)
        geo_pt2 = _ports.GeoPt(18, 100)
        geo_pt3 = _ports.GeoPt(-18, -100)
        geo_pt4 = _ports.GeoPt(0, 0)
        geo_pt5 = "1,2"
        geo_pt6 = 88.0
        geo_pt7 = unittest.mock.sentinel.geo_pt

        assert geo_pt1 == geo_pt1
        assert not geo_pt1 == geo_pt2
        assert not geo_pt1 == geo_pt3
        assert not geo_pt1 == geo_pt4
        assert not geo_pt1 == geo_pt5
        assert not geo_pt1 == geo_pt6
        assert not geo_pt1 == geo_pt7

    @staticmethod
    def test___lt__():
        geo_pt1 = _ports.GeoPt(-18, 100)
        geo_pt2 = _ports.GeoPt(18, 100)
        geo_pt3 = _ports.GeoPt(-18, -100)
        geo_pt4 = _ports.GeoPt(0, 0)
        geo_pt5 = "1,2"
        geo_pt6 = 88.0
        geo_pt7 = unittest.mock.sentinel.geo_pt

        assert not geo_pt1 < geo_pt1
        assert geo_pt1 < geo_pt2
        assert not geo_pt1 < geo_pt3
        assert geo_pt1 < geo_pt4
        assert geo_pt1 < geo_pt5
        with pytest.raises(TypeError):
            geo_pt1 < geo_pt6
        with pytest.raises(TypeError):
            geo_pt1 < geo_pt7

    @staticmethod
    def test___hash__():
        geo_pt = _ports.GeoPt(7.5, 77.5)
        assert hash(geo_pt) == hash((7.5, 77.5))

    @staticmethod
    def test___repr__():
        geo_pt = _ports.GeoPt(0.0, 0.0)
        assert repr(geo_pt) == "datastore_types.GeoPt(0.0, 0.0)"

    @staticmethod
    def test___str__():
        geo_pt = _ports.GeoPt(10.0, 10.0)
        assert str(geo_pt) == "10.0,10.0"

    @staticmethod
    def test_ToXml():
        geo_pt = _ports.GeoPt(5.0, -20.0)
        assert geo_pt.ToXml() == "<georss:point>5.0 -20.0</georss:point>"
