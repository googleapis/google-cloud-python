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

from google.cloud.ndb import _exceptions
from google.cloud.ndb import query
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(query)


def test_Cursor():
    assert query.Cursor is NotImplemented


class TestQueryOptions:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.QueryOptions()


class TestRepeatedStructuredPropertyPredicate:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.RepeatedStructuredPropertyPredicate()


class TestParameterizedThing:
    @staticmethod
    def test___eq__():
        thing = query.ParameterizedThing()
        with pytest.raises(NotImplementedError):
            thing == None

    @staticmethod
    def test___ne__():
        thing = query.ParameterizedThing()
        with pytest.raises(NotImplementedError):
            thing != None


class TestParameter:
    @staticmethod
    def test_constructor():
        for key in (88, b"abc", "def"):
            parameter = query.Parameter(key)
            assert parameter._key == key

    @staticmethod
    def test_constructor_invalid():
        with pytest.raises(TypeError):
            query.Parameter(None)

    @staticmethod
    def test___repr__():
        parameter = query.Parameter("ghi")
        assert repr(parameter) == "Parameter('ghi')"

    @staticmethod
    def test___eq__():
        parameter1 = query.Parameter("yep")
        parameter2 = query.Parameter("nope")
        parameter3 = unittest.mock.sentinel.parameter
        assert parameter1 == parameter1
        assert not parameter1 == parameter2
        assert not parameter1 == parameter3

    @staticmethod
    def test___ne__():
        parameter1 = query.Parameter("yep")
        parameter2 = query.Parameter("nope")
        parameter3 = unittest.mock.sentinel.parameter
        assert not parameter1 != parameter1
        assert parameter1 != parameter2
        assert parameter1 != parameter3

    @staticmethod
    def test_key():
        parameter = query.Parameter(9000)
        assert parameter.key == 9000

    @staticmethod
    def test_resolve():
        key = 9000
        bound_value = "resoolt"
        parameter = query.Parameter(key)
        used = {}
        result = parameter.resolve({key: bound_value}, used)
        assert result == bound_value
        assert used == {key: True}

    @staticmethod
    def test_resolve_missing_key():
        parameter = query.Parameter(9000)
        used = {}
        with pytest.raises(_exceptions.BadArgumentError):
            parameter.resolve({}, used)

        assert used == {}


class TestParameterizedFunction:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.ParameterizedFunction()


class TestNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.Node()


class TestFalseNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.FalseNode()


class TestParameterNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.ParameterNode()


class TestFilterNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.FilterNode()


class TestPostFilterNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.PostFilterNode()


class TestConjunctionNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.ConjunctionNode()


class TestDisjunctionNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.DisjunctionNode()


def test_AND():
    assert query.AND is query.ConjunctionNode


def test_OR():
    assert query.OR is query.DisjunctionNode


class TestQuery:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.Query()


def test_gql():
    with pytest.raises(NotImplementedError):
        query.gql()


class TestQueryIterator:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.QueryIterator()
